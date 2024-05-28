Email = document.getElementById("Email")
Password = document.getElementById("Password")
Re_Password = document.getElementById("Re-Password")

function reset(){
    Email.value = "";
    Password.value = "";
    Re_Password.value = "";
} 

function LogIn_User() {
    if (!Email.value){
        alert("Please Enter the Email")
        return
    }
    if (!Password.value){
        alert("Please Enter the Password")
        return
    }
    if (!Re_Password.value){
        alert("Please Enter the Re-Password")
        return
    }
    if (Password.value==Re_Password.value){
        const user_data = {
            "email": Email.value,
            "password": Password.value
        };
        const requestData = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user_data)
        };
        fetch("/",requestData).
            then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText);
                } 
            return response.json();
            })
            .then(data => {
                console.log(data)
                var token = data.token;
                sessionStorage.setItem('token', token);
                if (data.message) {
                    alert('LogIn Successfully')
                    var anchor = document.createElement("a");
                    anchor.href = "/api/open_dashboard";
                    anchor.click();
                }else {
                    alert(data.error)
                    reset()
                    return
                }
            })
            .catch(error => {
                alert("error:"+error.message)
            });

    } else {
        alert("Password didn't match please Re-Enter the matching password")
    }
}