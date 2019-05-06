from FSA.accountmodel.account import Account

def add_variable_to_context(request):
    user = request.session.get("SignInName")
    if request.session.get("SignInName"):
        user = request.session.get("SignInName")
        user = (Account.objects.all().filter(SignInName=user))[0]
        sessionID = user.groupid
    else:
        sessionID = -1
    return {
        'sessionID': sessionID
    }