const loginbtn=document.querySelector("#loginbtn");
if (loginbtn!=null){
  loginbtn.addEventListener('click',(e)=>{
    
    const mail=document.querySelector('.mail').value;
    const password=document.querySelector('.pass').value;
    if(password=='' || mail==''){
      const msg=document.querySelector('.login-msg');
      msg.innerHTML="Email and Password can not empty";
      msg.style.color="red";
    }else{
      const data={
        email: mail,
        password: password
      };
      fetch('user-authentication',{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }).then((response)=>{
        return response.json().then((data)=>{
          if (!response.ok){
            throw data
          }
          window.location.href = "/";
        })
      }).catch((e)=>{
        const msg=document.querySelector('.login-msg');
        msg.innerHTML=e.error
        msg.style.color="red"
      })
    }
  })
}