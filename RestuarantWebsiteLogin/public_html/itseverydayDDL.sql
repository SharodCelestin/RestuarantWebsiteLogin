CREATE TABLE Employee(
empid varchar(8) not null,
epasscode varchar (120) not null,
UNIQUE(empid),
ename varchar(15) not null,
Address varchar(50),
ephonenum numeric(10),
hoursworked  numeric(2) check (hoursworked > 0),
position varchar(10),
payrate numeric(4,2) check (payrate > 0),
primary key (empid)
);
CREATE TABLE menuitem(
menuitemid varchar(8) not null,
UNIQUE(menuitemid),
miname varchar(15) not null,
price numeric(4,2) check (price > 0),
mitemtype varchar(8),
primary key (menuitemid)

);
CREATE TABLE Customer(
cusid varchar(8) not null,
UNIQUE(cusid),
cusname varchar(15) not null,
cusphonenum numeric(10),
cpasscode varchar(120),
Address varchar(50),
empid varchar(8) not null,
menuitemid varchar(8)  not null,
primary key (cusid),
foreign key (empid) references Employee 
on delete set null,
foreign key (menuitemid) references menuitem 
on delete set null
);
CREATE TABLE orders(
orderid varchar(8)  not null,

UNIQUE(orderid),
amount numeric(6,2) check (amount > 0),
Instructions varchar(200),
Paymenttype varchar(10),
cusid varchar(8) not null,
primary key(orderid),
foreign key(cusid) references Customer
on delete set null
);
CREATE TABLE isTakenby(
orderid varchar(8) not null,
empid varchar(8) not null,
foreign key (orderid) references orders
on delete set null,
foreign key (empid) references Employee
on delete set null

);

CREATE TABLE inventory(
inventoryid varchar(8) not null,
UNIQUE(inventoryid),
Sales numeric(6,2) check (Sales > 0),
Profit numeric(6,2),
empid varchar(8) not null,
primary key (inventoryid),
foreign key (empid) references Employee
on delete set null
);
CREATE TABLE items(
Itemid varchar(8) not null,
UNIQUE(Itemid),
Itemname varchar(15) not null,
Itemquantity numeric(5) check (Itemquantity>0),
Cost numeric(5,2) check (Cost>=0),
Expirationdate date,
primary key(Itemid)

);
CREATE TABLE supplier(
suppliername varchar(15) not null,
supplierid varchar(8) not null,
UNIQUE(supplierid),
sphonenum numeric(10),
saddress varchar(50),
suppliertype varchar(10),
primary key(supplierid)
);
CREATE TABLE delivers(
supplierid varchar(8) not null,
Itemid varchar(8) not null,
Deliverydate date,
foreign key (Itemid) references items
on delete set null,
foreign key (supplierid) references supplier
on delete set null

);
CREATE TABLE consistof(
menuitemid varchar(8) not null,
Itemid varchar(8) not null,
foreign key (Itemid) references items
on delete set null,
foreign key (menuitemid) references menuitem
on delete set null
);
CREATE TABLE contain(
orderid varchar(8) not null,
menuitemid varchar(8) not null,
foreign key (orderid) references orders
on delete set null,
foreign key (menuitemid) references menuitem
on delete set null
);
