from ferris import Controller, route_with, messages
from app.models.car import Car
from app.models.reservation import Reservation
from app.models.user.user import User
from google.appengine.api import users
from google.appengine.ext import deferred
from ferris.core import mail
import json
import logging
import datetime
import uuid


class Reservations(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = Reservation

    @route_with('/api/reservations/:<key>', methods=['POST'])
    def api_reserve(self, key):
        params = json.loads(self.request.body)
        params['car'] = self.util.decode_key(key)
        params['renter'] = User.get(params['renter'], key_only=True)
        params['pickup_date'] = datetime.datetime.strptime(params['pickup_date'].split('T')[0], '%Y-%m-%d')
        params['dropoff_date'] = datetime.datetime.strptime(params['dropoff_date'].split('T')[0], '%Y-%m-%d')
        params['request_code'] = code_generator()
        params['amount'] = 12.12
        Reservation.create(**params)
        return 200

    @route_with('/api/reservations/pending', methods=['GET'])
    def api_list(self):
        lis = Reservation.list(False)
        if lis:
            self.context['data'] = lis
        else:
            return 200

    @route_with('/api/reservations/:<key>', methods=['GET'])
    def api_get(self, key):
        self.context['data'] = self.util.decode_key(key).get()

    @route_with('/api/reservations/:<key>/<vendor>', methods=['PUT'])
    def api_update(self, key, vendor):
        params = json.loads(self.request.body)
        request = self.util.decode_key(key).get()
        request.update(**params)
        car = self.util.decode_key(request.car.urlsafe()).get()
        deferred.defer(send_mail, request, car, vendor)
        return 200


def code_generator():
    return str(uuid.uuid4())[0:8]

def send_mail(request, car, vendor):
    try:
        renter = request.renter.id()
        logging.info("Sending email to %s"%renter)
        subject = "CarE Rental Booking Status"
        template = """
        <table cellpadding="5">
            <thead>
            <tr>
                <td>Transaction Code</td>
                <td>Car</td>
                <td>Vendor</td>
                <td>Price</td>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            </tbody>
        </table>
        """ % (request.request_code, car.car_model, vendor, request.amount)
        body = """Hi, <br><br>
                      Your booking request was %s. <br>
                      Here are the details of transaction: <br><br>
                      %s""" % ("approved" if request.rejected else "rejected", template)
        mail.send(renter, subject, body)
    except Exception, e:
        logging.info("########-------->>>>>>")
        logging.info(str(e))
