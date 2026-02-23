const registrationBtn=document.querySelector("#registrationBtn");
const cpassword=document.querySelector(".cpassword");
const checkbox=document.querySelector(".checkbox");
const msg=document.querySelector(".msg");
checkbox.addEventListener('change',(e)=>{
  if(checkbox.checked){
    console.log('a')
    cpassword.type='text';
  }else{
    console.log('b')
    cpassword.type='password';
  }
})

registrationBtn.addEventListener('click',(e)=>{
  const fname=document.querySelector("#fname").value;
  const lname=document.querySelector("#lname").value;
  const email=document.querySelector(".email").value;
  const password=document.querySelector(".password").value;
  const pincode=document.querySelector(".pincode").value;
  msg.style.display='block';
  msg.style.color='red';
  if(fname=='' || lname=='' || email=='' || password=='' || cpassword.value=='' || pincode==''){
    msg.innerHTML='You have to filled all the entries'
  }
  else if(password!=cpassword.value){
    msg.innerHTML="Password and confirm password is not matched."
  }else{
    const data={
      fname: fname,
      lname: lname,
      email: email,
      password: password,
      cpassword: cpassword,
      pincode: pincode
    }
    fetch('validate-registration',{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then((response)=>{
      return response.json()
    }).then((data)=>{
      console.log(data)
    }).catch((e)=>{
      console.log(e)
    })
  }
});