FirstName = document.getElementById("FirstName")
LastName = document.getElementById("LastName")
Email = document.getElementById("Email")
Password = document.getElementById("Password")
Re_Password = document.getElementById("Re-Password")
function reset(){
    FirstName.value = "";
    Email.value = "";
    Password.value = "";
    Re_Password.value = "";
} 
function register_User(){
    // this function is used for collect the data from register form and send to backend
    if (Password.value.length < 7) {
        alert("password length should be more then 8 charectors")
    }else {
        if (Password.value == Re_Password.value){
            const user_data = {
                "firstname": FirstName.value,
                "lastname": LastName.value,
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
            fetch("/api/register",requestData).
            then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText)
                } 
                return response.json()
            })
            .then(data =>{
                console.log(data)
                if (data.message) {
                    alert('Registered Successfully')
                    var anchor = document.createElement("a");
                    anchor.href = "/";
                    anchor.click();
                }else {
                    alert(data.error)
                    reset()
                }
            })
            .catch(error => {
                alert("error:",error)
            })
        } else {
            alert("Password didn't match please Re-Enter the matching password")
        }
    }
}