from flask import session,redirect
def logout():
    session["email"] = None
    session["subject"] = None
    session['question']=None
    session['notice']=None
    session['answer']=None
    session['explain']=None
    session['num_aws_cp']=None
    session['num_aws_saa']=None
    session['answered_total']=None
    session['answered_correct']=None
    return redirect("/")