const registrationBtn = document.querySelector("#registrationBtn");
const cpassword = document.querySelector(".cpassword");
const checkbox = document.querySelector(".checkbox");
const msg = document.querySelector(".msg");

checkbox.addEventListener("change", () => {
  cpassword.type = checkbox.checked ? "text" : "password";
});

registrationBtn.addEventListener("click", (e) => {
  e.preventDefault(); 

  const fname = document.querySelector("#fname").value;
  const lname = document.querySelector("#lname").value;
  const email = document.querySelector(".email").value;
  const password = document.querySelector(".password").value;
  const phone = document.querySelector(".phone").value;

  msg.style.color = "red";
  if(fname=='' || lname=='' || email=='' || password=='' || cpassword.value=='' || phone==''){
    msg.classList.remove("d-none")
    msg.innerHTML='You have to filled all the entries'

  } 
  else if(password!=cpassword.value){
    msg.classList.remove("d-none")
    msg.innerHTML="Password and confirm password is not matched."
  }else{
    const data = {
      fname,
      lname,
      email,
      password,
      cpassword: cpassword.value,
      phone
    };

    fetch("validate-registration", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
          throw new Error(data.error);
        }
        return data;
    }))
    .then(data => {
        console.log("Success:", data);
        msg.classList.remove("d-none")
        msg.innerHTML = data.error;
    })
    .catch(error => {
        msg.classList.remove("d-none")
        msg.innerHTML = error.message;  
    });
  }  
});