Email = document.getElementById("Email")
function forgetPassword() {
    const user_data = {
        "email": Email.value,
    };
    const requestData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user_data)
    };
    fetch("/api/forget_password",requestData).
        then(response => {
            if (!response.ok) {
                throw new Error('Email is Not there or Provide correct email') 
            }
            return response.json()
        })
        .then(data=>{     
            alert("Sent Reset Email to Your Mail")
            sessionStorage.setItem('email',data['email'])
            var anchor = document.createElement("a");
            anchor.href = "/api/open_initiate";
            anchor.click();
        }).catch(error=>{
            alert(error)
        })
}
        

function changePassword() {
    Password = document.getElementById("Password")
    console.log(sessionStorage.getItem('email'))
    const user_data = {
        "email":sessionStorage.getItem('email'),
        "password": Password.value
    };
    const requestData = {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user_data)
    };
    fetch("/api/forget_password",requestData).
        then(response => {
            if (!response.ok) {
                throw new Error('Incorrect eamil');
            }
            return response.json();
        })
        .then(data => {
            var token = data.token;
            sessionStorage.setItem('token', token);
            alert("Password Changed successfully")
            var anchor = document.createElement("a");
            anchor.href = "/";
            anchor.click();
        })
        .catch(error=>{
            alert(error)
        })
}
