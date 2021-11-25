function register_validation() 
    {
    var password1 = document.getElementById("password1");
    var password2 = document.getElementById("password2");
    if (password1.value.length < 6) 
        {alert ("Password must be at least 6 characters in length!");
        return false;}
    if (password2.value != password1.value) 
        {alert ("Passwords do not match!");
        return false;}

    return true;
    }