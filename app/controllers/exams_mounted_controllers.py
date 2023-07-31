from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField, RadioField, TextAreaField, HiddenField, SelectMultipleField, fields, FileField, datetime, DateTimeField, DateField, TimeField 
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from datetime import datetime

from ..models import Exam, Question, User, Exam_mounted
from flask_login import login_required, current_user, login_url, logout_user, login_manager, UserMixin, AnonymousUserMixin, set_login_view
from functools import wraps

bp_name = "exams_mounted"

print(f"Loading {__file__}...")
print(f"bp_name = {bp_name}")


bp = Blueprint(bp_name, __name__)
from ..webapp import db

properties = {
    "entity_name": "exam_mounted",
    "collection_name": "exams_mounted",
    "list_fields": ["id","title", "exam_id", "question_id", "question_worth", "Is it open?", "start_date", "end_date"]
}

################     test admin access control    #####################
EXEMPT_METHODS = {"OPTIONS"}
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        
        if request.method in EXEMPT_METHODS or current_app.config.get("LOGIN_DISABLED"):
            pass
        elif current_user.is_student:
            current_app.login_manager.LOGIN_MESSAGE = "only admin may access this page."
            return current_app.login_manager.unauthorized()
            #return current_app.login_manager.LOGIN_MESSAGE

        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view
############################################################################


class _to:
    def __to(method):
        return lambda **kwargs: url_for(f"{bp_name}.{method}", **kwargs)

    index = __to("index")
    show = __to("show")
    edit = __to("edit")
    delete = __to("delete")


class _j:
    index = f"{bp_name}/index.jinja2"
    edit = f"{bp_name}/edit.jinja2"
    show = f"{bp_name}/show.jinja2"
    new = f"{bp_name}/new.jinja2"
    create = f"{bp_name}/create.jinja2"
    search_tmdb = f"{bp_name}/search_tmdb.jinja2"
    
    




@bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Index page.
    :return: The response.
    """    
    exams_mounted = Exam_mounted.query.all()
    print( "current_user = ", current_user)
    return render_template(_j.index, entities=exams_mounted, **properties)


    
class EditForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    exam_id = SelectField("exam", choices=[], coerce = int)
    question_id = SelectField("question", choices=[], coerce = int)
    question_worth = IntegerField("question_worth")    
    
    start_date = DateTimeField("start_date")
    end_date = DateTimeField("end_date")            

    comments = StringField("Is it Open?")
    
    submit = SubmitField("Submit")
    
# @bp.route("/", methods=["GET", "POST"])
# def check_hours():
#     form = EditForm()
    
#     end_date = form.end_date.data
#     current_time = datetime.now()
    
#     if current_time > end_date:
#         comments = "Already Closed!"
#     else:
#         comments ="It's open!"
        
#     return render_template(_j.show, entity=exams_mounted, **properties)
    
class SearchForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    submit = SubmitField("Submit")


@bp.route("/new", methods=["GET"])                 # decorator test to check if user is logged in to create new exam_mounted 
@admin_required
def new():
    """
    Page to create new Entity
    :return: render create template
    """
    form = EditForm()
    form.exam_id.choices = [(exam.id, exam.title) for exam in Exam.query.all()]
    
    # append questions to form 
    form.question_id.choices = [(question.id, question.title) for question in Question.query.all()]
    
    return render_template(_j.new, form=form, **properties)


@bp.route("/", methods=["POST"])
@admin_required
def create():
    """
    Create new entity
    :return: redirect to view new entity
    """
    form = EditForm(formdata=request.form)
    #if form.validate_on_submit():
    newexam_mounted = Exam_mounted()
    form.populate_obj(newexam_mounted)
    db.session.add(newexam_mounted)
    db.session.commit()
    flash(f"'{ newexam_mounted.title}' created")
    return redirect(_to.show(id=newexam_mounted.id))
    # else:
    #     flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    print( "current_user = ", current_user)
    exam_mounted = db.get_or_404(Exam_mounted, id)
    return render_template(_j.show, entity=exam_mounted, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
@admin_required
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    userform = EditForm(formdata=request.form, obj=exam_mounted)
    
    userform.exam_id.choices = [(exam.id, exam.title) for exam in Exam.query.all()]
    # append questions to form 
    userform.question_id.choices = [(question.id, question.title) for question in Question.query.all()]
    
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
@admin_required
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    form = EditForm(formdata=request.form, obj=exam_mounted)
    # if form.validate_on_submit():
    form.populate_obj(exam_mounted)
    db.session.commit()
    flash(f"'{ exam_mounted.title}' updated")
    return redirect(_to.show(id=id))
    # else:
    #     flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
@admin_required
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    db.session.delete(exam_mounted)
    db.session.commit()
    flash(f"'{ exam_mounted.title}' deleted")
    return redirect(_to.index())


#route only for students to answer exams
@bp.route("/<int:id>/answer", methods=["GET", "POST"])  #TODO: implement this route
def answer(id): 
    return f"id = {id} : to do"
