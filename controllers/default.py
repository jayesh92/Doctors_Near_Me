# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

@auth.requires_login()
def index():
    doctors = db().select(db.doctors.ALL, orderby=db.doctors.name)
    locality={}
    for doctor in doctors:
        locality[doctor.locality]=1
    return dict(doctors=doctors,locality=locality)

def error():
    return dict()
    
def add_doctor():
    form = SQLFORM(db.doctors)
    if form.process().accepted:
        redirect(URL(r=request,f='index'))
    elif form.errors:
          response.flash = 'Plz enter all fields'
    return dict(form=form)
    
def show():
    doctor=db(db.doctors.id==request.args(0)).select()[0]
    comment=db().select(db.comments.ALL)
    image=db().select(db.images.ALL)
    form = SQLFORM(db.comments,fields=['body'])
    form.vars.doctor_id = request.args(0)
    form.vars.author=auth.user.username
    if form.accepts(request.vars, session):
        redirect(URL(r=request,f='show',args=request.args(0)))
        response.flash = 'Your Comment is Posted'    
    return dict(doctor=doctor,comment=comment,image=image,form=form)
    
def download():
    return response.download(request,db)
    
def uncomment():
    db(db.comments.id == request.args(0)).delete()
    redirect(URL(r=request,f='show',args=request.args(1)))
    response.flash = 'Comment Deleted'
    
def add_image():
    form = SQLFORM(db.images,fields=['file'])
    form.vars.doctor_id=request.args(0)
    if form.process().accepted:
        redirect(URL(r=request,f='show',args=request.args(0)))
    elif form.errors:
          response.flash = 'Plz enter all fields'
    return dict(form=form)
