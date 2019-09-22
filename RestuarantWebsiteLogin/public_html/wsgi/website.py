import os
import web
from passlib.hash import pbkdf2_sha256

web.config.debug = False
from jinja2 import Environment, FileSystemLoader
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                             'templates')),
                                extensions=extensions)
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)
    web.header('Cache-Control',
               'no-cache, max-age=0, must-revalidate, no-store',
               unique=True
    )

    return jinja_env.get_template(template_name).render(context)

render = web.template.render('/home/itseveryday/public_html/wsgi/templates/')
db = web.database(dbn = 'postgres', user = 'itseveryday',pw = 'Guccigang101',db= 'itseveryday')
urls = (
'/','index',
'/eregister','eregister',
'/cregister','cregister',
'/elogin','elogin',
'/einfo','einfo',
'/eloggedout','eloggedout',
'/cpage','cpage',
'/clogin','clogin',
'/order','order'






)
app = web.application(urls, globals())

session = web.session.Session(app,
          web.session.DiskStore('/var/lib/php/session'),
              initializer={'loggedIn' : False, 'empid' : ''}
          )
customers = ' '
class index:
	def GET(self):
		employees = db.select('employee')
		return render.index(employees)

class eregister:
	def GET(self):
		return render_template('eregister.html')
	def POST(self):
		epasscode,ename,address,ephonenum,position = web.input().epasscode,web.input().ename,web.input().address,web.input().ephonenum,web.input().position
		
		empids= db.select('employee',what='max(empid)')
		
		print(empids)
		
		empid=0
		try:
			for maxi in empids:
				if maxi.max > empid:
					empid = maxi.max
			addone = int(empid) + 1 
			empid = str(addone)
		except:
			empid=1
	
		hoursworked = 0.5
		payrate = 10
		hash = pbkdf2_sha256.hash(epasscode)
		pbkdf2_sha256.verify(epasscode,hash)
		query = 'insert into employee values ($empid,$epasscode,$ename,$address,$ephonenum,$hoursworked,$position,$payrate);'
		values = { 'empid': empid, 'epasscode' : hash ,'ename' : ename ,'address' : address ,'ephonenum'  :ephonenum  ,'hoursworked' : hoursworked ,'position' : position , 'payrate' : payrate}
		n = db.query(query,values)
		session.loggedIn = True
		session.empid = empid
		return render_template('einfo.html',empid = session.empid)
		#raise web.seeother('/')
			
class cregister:
	def GET(self):
		menuitem = db.select('menuitem')
		return render.cregister(menuitem)
	def POST(self):
		cusname,address,cusphonenum,miname = web.input().cusname,web.input().address,web.input().cusphonenum,web.input().miname
		deliverypersonname ='none'
		names = ' '
		names = miname
		vars = dict(miname=names)
		mitemids= db.select('menuitem',what = 'menuitemid',where = "miname = $miname",vars=vars)
		menuitemid =0
		for item in mitemids:
			menuitemid = item.menuitemid
			
		customernames= db.select('customer',what = 'cusname')
		cusid = 0
		try:
			for names in customernames:
				if names.cusname == cusname:
							return '<h3>A person with name ' + cusname + ' already exist. Choose another name </h3>'
			addone = int(cusid)+1 
			cusid = str(addone)
		except:
			print("It's not working")
			
		maxcusid = db.select('customer',what = 'max(cusid)')
		try:
			for ids in maxcusid:
				if ids.max > cusid:
					cusid = ids.max
			addone = int(cusid)+1 
			cusid = str(addone)
		except:
			print("cus id is not incremented")
		
		query = 'insert into customer values($cusid,$cusname,$cusphonenum,$address,$menuitemid,$deliverypersonname)';
		values = { 'cusid': cusid,'cusname' : cusname, 'cusphonenum' :cusphonenum, 'address' :address , 'menuitemid' : menuitemid , 'deliverypersonname':deliverypersonname} 
		n = db.query(query,values)
		#raise web.seeother('/')
		cid = cusid
		vars = dict(cusid = cid)
		customers = db.select('customer',what = '*',where = "cusid = $cusid",vars = vars)
		menuitem =db.select('menuitem')
		return render.cpage(customers,menuitem)
			
class elogin:
	def GET(self):
		if session.loggedIn:
			return render_template('einfo.html',empid = session.empid)
		else:
			return render_template('elogin.html')
			
	def POST(self):	
		empid,epasscode = web.input().empid,web.input().epasscode
		ids = ' '
		ids = empid
		vars = dict(empid = ids)
		#try:
		query = db.select('employee',what = '*', where = "empid = $empid",vars=vars)[0]
		
		#hash = pbkdf2_sha256.hash(epasscode)
		#epasscode = str(hash)	
		#for password in query:
		if pbkdf2_sha256.verify(epasscode,query['epasscode']):
			print("After if")
			session.loggedIn = True
			session.empid = empid
			return render_template('einfo.html',empid = session.empid)
		else:
			return 'Your username or password is wrong. Go back and try again.'
				#return 'Hello'
	
				#pass
		#raise web.seeother('/')
class einfo:
    def GET(self):
        if session.loggedIn:
           return render_template('einfo.html', empid=session.empid)
           #return render.template('einfo.html')
        else:
           raise web.seeother('/')
class eloggedout:
	def GET(self):
		if session.loggedIn:
			session.loggedIn = False
			return render_template('eloggedout.html',empid= session.empid)
class clogin:
	def GET(self):
		return render_template('clogin.html')
	def POST(self):
		try:
			cusname = web.input().cusname
			name = ' '
			name = cusname
			vars = dict(cusname = name)
		
			customers = db.select('customer',what = '*', where = "cusname = $cusname",vars=vars)
			for cname in customers:
				if cname.cusname == cusname:
					customers = db.select('customer',what = '*', where = "cusname= $cusname",vars=vars)
					menuitem = db.select('menuitem')
					print('Its working till here')
					return render.cpage(customers,menuitem)
				else:
					return '<h3>You typed in the wrong name</h3>'
		except:
			return '<h3>You typed in the wrong name</h3>'
class cpage:
	def GET(self):
		menuitem = db.select('menuitem')
		return render_template('cpage.html',customers,menuitem)
	def POST(self):
		cusid, instructions,paymenttype,menuitems= web.input().cusid,web.input().instructions,web.input().paymenttype,web.input(menuitemid=[]).menuitemid
		print('Menuitems:', menuitems)
		orderid = 100
		try:
			maxorderid = db.select('orders',what = 'max(orderid)')
			for maxi in maxorderid:
				if maxi.max > orderid:
					orderid = maxi.max
			addone = int(orderid) + 1 
			orderid = str(addone)	
		except:
			orderid = 100
		amount = 0.00
		print("before the for loop")
		for items in menuitems:
			print(items)
			item= ' '
			item = items
			vars = dict(items = item)
			prices = db.select('menuitem',what='price',where = "menuitemid = $items",vars = vars)
			for p in prices:
				amount += float(p.price)
		
		query = 'insert into orders values($orderid,$amount,$instructions,$paymenttype,$cusid)';
		values = { 'orderid': str(orderid) , 'amount' : amount , 'instructions' : instructions , 'paymenttype' : paymenttype , 'cusid' : cusid }
		n = db.query(query,values)
		orders = db.select('orders')
		return render.order(orders)
		
class order:
	def GET(self):
		orders = db.select('orders')
		return render_tempate('order.html',orders)
		
				
		
if __name__ == "__main__":
	app.run()
else:
	application = app.wsgifunc() 
