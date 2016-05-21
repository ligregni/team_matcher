from flask import render_template, flash, redirect, request
from app import app
from forms import InputForm
from team_matcher import get_calendar

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if request.method == 'POST':
    #if form.validate_on_submit():
        flash(str(request.args.get('number_of_teams')))
        return redirect(
            '/calendar?number_of_teams={}'.format(
                request.form['number_of_teams']))
    return render_template('main.html', title='Team Matcher', form=form)

@app.route('/calendar', methods=['GET'])
def calendar():
    n = int(request.args.get('number_of_teams'))
    return render_template(
            'calendar.html',
            title='Teams Calendar',
            number_of_teams=n,
            calendar=get_calendar(n))
