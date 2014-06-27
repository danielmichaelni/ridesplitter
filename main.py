#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
from google.appengine.ext import db

import datetime


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

'''class Rides(db.Model):
	pickup_datetime = db.DateTimeProperty(required = True)
	location = db.StringProperty(required = True)
	destination = db.StringProperty(required = True)
	riders = db.ListProperty(str, default = None, required = True)
	numbers = db.ListProperty(str, default = None)
	emails = db.ListProperty(str, default = None)'''

class OHareRides(db.Model):
	pickup_datetime = db.DateTimeProperty(required = True)
	location = db.StringProperty(required = True)
	riders = db.ListProperty(str, default = None, required = True)
	numbers = db.ListProperty(str, default = None)
	emails = db.ListProperty(str, default = None)
	luggage = db.ListProperty(str, default = None)
	code = db.ListProperty(str, default = None)
	comments = db.StringProperty()

class MidwayRides(db.Model):
	pickup_datetime = db.DateTimeProperty(required = True)
	location = db.StringProperty(required = True)
	riders = db.ListProperty(str, default = None, required = True)
	numbers = db.ListProperty(str, default = None)
	emails = db.ListProperty(str, default = None)
	luggage = db.ListProperty(str, default = None)
	code = db.ListProperty(str, default = None)
	comments = db.StringProperty()

def check_beta_code(code):
	if code == "uchicago2014":
		return True
	return False

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
    	return t.render(params)
    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		beta_code = self.request.cookies.get("beta_code")
		if check_beta_code(beta_code):
			self.render("index.html")
		else:
			self.render("beta_code.html")
	def post(self):
		beta_code = str(self.request.get('beta_code'))
		self.response.headers.add_header('Set-Cookie', 'beta_code=%s' % beta_code)
		if(check_beta_code(beta_code)):
			self.render("index.html")
		else:
			self.get()

class Browse(Handler):
	def get(self):
		#rides = db.GqlQuery("select * from Rides order by pickup_datetime asc")
		#self.render("browse.html", rides=rides)
		self.render("browse.html")
	'''def post(self):
		add_ride = self.request.get("add_ride_button")
		join_ride = self.request.get("join_ride_button")
		if add_ride:
			self.add_ride()
		elif join_ride:
			self.join_ride()
		else:
			self.write("error")'''

	#def render_rides(self, date="", time="", location="", destination="", name="", phone=""):
	#	rides = db.GqlQuery("select * from Rides order by pickup_datetime asc")
	#	self.render("browse.html", rides=rides, date=date, time=time, location=location, destination=destination, name=name, phone=phone)

	'''def add_ride(self):
		date_parts = self.request.get("date")
		time_parts = self.request.get("time")
		location = self.request.get("location")
		destination = self.request.get("destination")
		name = self.request.get("name")
		phone = self.request.get("phone")
		luggage = self.request.get("luggage")
		if date_parts and time_parts and location and destination and name and phone and luggage:
			date_parts_list = date_parts.split('-')
			time_parts_list = time_parts.split(':')
			if(date_parts_list < 1900):
				error = "invalid year"
				self.render_rides(date=date, time=time, location=location, destination=destination, name=name, phone=phone)
			else:
				pickup_datetime = datetime.datetime(int(date_parts_list[0]), int(date_parts_list[1]), int(date_parts_list[2]), int(time_parts_list[0]), int(time_parts_list[1]))
				r = Rides(pickup_datetime=pickup_datetime, location=location, destination=destination, luggage=luggage)
				r.riders.append(name)
				r.numbers.append(phone)
				r.put()
				self.redirect('/browse')
		else:
			error = "must complete all fields"
			self.render_rides(date=date, time=time, location=location, destination=destination, name=name, phone=phone)
	def join_ride(self):
		join_name = self.request.get("join_name")
		join_phone = self.request.get("join_phone")
		join_email = self.request.get("join_email")
		if not join_phone:
			join_phone = "N/A"
		if not join_email:
			join_email = "N/A"
		ride_id = self.request.get("get_ride_id")
		r = Rides.get_by_id(int(ride_id))
		r.riders.append(join_name)
		r.numbers.append(join_phone)
		r.emails.append(join_email)
		r.put()
		self.redirect('/browse')'''

class BrowseOHare(Handler):
	def get(self):
		beta_code = self.request.cookies.get("beta_code")
		if check_beta_code(beta_code):
			self.render_rides()
		else:
			self.redirect('/')
	def post(self):
		beta_code_button = self.request.get('beta_code_button')
		join_ride_button = self.request.get('join_ride_button')
		delete_rider_button = self.request.get('delete_rider_button')
		if beta_code_button:
			beta_code = str(self.request.get('beta_code'))
			self.response.headers.add_header('Set-Cookie', 'beta_code=%s' % beta_code)
			if(check_beta_code(beta_code)):
				self.render_rides()
			else:
				self.get()
		elif join_ride_button:
			self.join_ride()
		elif delete_rider_button:
			self.delete_rider()
		else:
			self.write("error")
	def delete_rider(self):
		rider_id = int(self.request.get("get_rider_id"))
		ride_id = self.request.get("get_delete_ride_id")
		r = OHareRides.get_by_id(int(ride_id))
		input_delete_code = self.request.get("delete_code")
		if input_delete_code == r.code[rider_id] or input_delete_code == "1q2w12":
			r.riders.pop(rider_id)
			r.numbers.pop(rider_id)
			r.emails.pop(rider_id)
			r.luggage.pop(rider_id)
			r.code.pop(rider_id)
			r.put()
			self.redirect('/browse/ohare')
		else:
			self.write("wrong code")
	def render_rides(self):
		orides = db.GqlQuery("select * from OHareRides order by pickup_datetime asc")
		self.render("browse_airport.html", airport="O'Hare", rides=orides)
	def join_ride(self):
		join_name = self.request.get("join_name")
		join_phone = self.request.get("join_phone")
		join_email = self.request.get("join_email")
		join_luggage = self.request.get("join_luggage")
		join_code = self.request.get("join_code")
		if not join_name or not join_email or not join_luggage or not join_code:
			self.write("ERROR: DID NOT ENTER NAME AND EMAIL AND LUGGAGE AND DELETE CODE")
		else:
			if not join_phone:
				join_phone = "N/A"
			ride_id = self.request.get("get_ride_id")
			r = OHareRides.get_by_id(int(ride_id))
			r.riders.append(join_name)
			r.numbers.append(join_phone)
			r.emails.append(join_email)
			r.luggage.append(join_luggage)
			r.code.append(join_code)
			r.put()
			self.redirect('/browse/ohare')

class BrowseMidway(Handler):
	def get(self):
		beta_code = self.request.cookies.get("beta_code")
		if check_beta_code(beta_code):
			self.render_rides()
		else:
			self.redirect('/')
	def post(self):
		beta_code_button = self.request.get('beta_code_button')
		join_ride_button = self.request.get('join_ride_button')
		delete_rider_button = self.request.get('delete_rider_button')
		if beta_code_button:
			beta_code = str(self.request.get('beta_code'))
			self.response.headers.add_header('Set-Cookie', 'beta_code=%s' % beta_code)
			if(check_beta_code(beta_code)):
				self.render_rides()
			else:
				self.get()
		elif join_ride_button:
			self.join_ride()
		elif delete_rider_button:
			self.delete_rider()
		else:
			self.write("error")
	def delete_rider(self):
		rider_id = int(self.request.get("get_rider_id"))
		ride_id = self.request.get("get_delete_ride_id")
		r = MidwayRides.get_by_id(int(ride_id))
		input_delete_code = self.request.get("delete_code")
		if input_delete_code == r.code[rider_id]:
			r.riders.pop(rider_id)
			r.numbers.pop(rider_id)
			r.emails.pop(rider_id)
			r.luggage.pop(rider_id)
			r.code.pop(rider_id)
			r.put()
			self.redirect('/browse/midway')
		else:
			self.write("wrong code")
	def render_rides(self):
		mrides = db.GqlQuery("select * from MidwayRides order by pickup_datetime asc")
		self.render("browse_airport.html", airport="Midway", rides=mrides)
	def join_ride(self):
		join_name = self.request.get("join_name")
		join_phone = self.request.get("join_phone")
		join_email = self.request.get("join_email")
		join_luggage = self.request.get("join_luggage")
		join_code = self.request.get("join_code")
		if not join_name or not join_email or not join_luggage or not join_code:
			self.write("ERROR: DID NOT ENTER NAME AND EMAIL AND LUGGAGE AND DELETE CODE")
		else:
			if not join_phone:
				join_phone = "N/A"
			ride_id = self.request.get("get_ride_id")
			r = MidwayRides.get_by_id(int(ride_id))
			r.riders.append(join_name)
			r.numbers.append(join_phone)
			r.emails.append(join_email)
			r.luggage.append(join_luggage)
			r.code.append(join_code)
			r.put()
			self.redirect('/browse/midway')

class Add(Handler):
	def get(self):
		beta_code = self.request.cookies.get("beta_code")
		if check_beta_code(beta_code):
			self.render("add.html")
		else:
			self.redirect('/')
	def post(self):
		beta_code_button = self.request.get("beta_code_button")
		add_ride_button = self.request.get("add_ride_button")
		if beta_code_button:
			beta_code = str(self.request.get('beta_code'))
			self.response.headers.add_header('Set-Cookie', 'beta_code=%s' % beta_code)
			if(check_beta_code(beta_code)):
				self.render("add.html")
			else:
				self.get()
		elif add_ride_button:
			self.add_ride()
		else:
			self.write("error")

	def add_ride(self):
		month = self.request.get("month")
		day = self.request.get("day")
		year = self.request.get("year")
		hour = self.request.get("hour")
		minute = self.request.get("minute")
		am_pm = self.request.get("am_pm")
		location = self.request.get("location")
		destination = self.request.get("destination")
		name = self.request.get("name")
		phone = self.request.get("phone")
		email = self.request.get("email")
		luggage = self.request.get("luggage")
		code = self.request.get("code")
		comments = self.request.get("comments")
		#if month and day and year and hour and minute and am_pm and destination and name and phone and email:
		if month and day and year and hour and minute and am_pm and destination and name and email and code and luggage:
			try:
				if int(hour) == 12:
					hour = int(hour) - 12
				pickup_datetime = datetime.datetime(int(year), int(month), int(day), int(hour) + 12 * int(am_pm), int(minute))
				if not phone:
					phone = "N/A"
				if destination == "ohare":
					oride = OHareRides(pickup_datetime=pickup_datetime, location=location, comments=comments)
					oride.riders.append(name)
					oride.numbers.append(phone)
					oride.emails.append(email)
					oride.luggage.append(luggage)
					oride.code.append(code)
					oride.put()
				if destination == "midway":
					mride = MidwayRides(pickup_datetime=pickup_datetime, location=location, comments=comments)
					mride.riders.append(name)
					mride.numbers.append(phone)
					mride.emails.append(email)
					mride.luggage.append(luggage)
					mride.code.append(code)
					mride.put()
				self.redirect('/browse/%s' % destination)
			except ValueError:
				error = "invalid date"
				self.handle_error(error=error, location=location, name=name, phone=phone, email=email)
		else:
			error = "must complete all fields"
			self.handle_error(error=error, location=location, name=name, phone=phone, email=email)
	
	def handle_error(self, error="", location="", name="", phone="", email=""):
		self.render("add.html", error=error, location=location, name=name, phone=phone, email=email)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/browse', Browse),
                               ('/browse/ohare', BrowseOHare),
                               ('/browse/midway', BrowseMidway),
                               ('/add', Add)],
                              debug=True)