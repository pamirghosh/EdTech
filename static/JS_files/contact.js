const btn=document.querySelector("#sendbtn");
btn.addEventListener('click',(e)=>{
  const fname=document.querySelector("#fname").value;
  const lname=document.querySelector("#lname").value;
  const email=document.querySelector(".email").value;
  const msg=document.querySelector(".msg").value;
  if(fname=='' || lname=='' || email=='' || msg==''){
    showErrMsg();
  }else{
    let data={
      fname: fname,
      lname: lname,
      email: email,
      message: msg
    };
    fetch('contact',{
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then((response)=>{
      if(!response)
        throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    }).then((data)=>{
      console.log(data)
    }).catch((error)=>{
      console.error('Error:', error); 
    });
  }
})
function showErrMsg(){
  const err_msg=document.querySelectorAll(".hide-prop");
  
  err_msg.forEach((el) => {
    el.classList.remove("hide-prop");
    el.classList.add("show-prop");
  });
}