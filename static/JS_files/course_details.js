const courses=document.querySelectorAll(".course");

courses.forEach(course => {
  course.addEventListener("click", function () {
    const course_id = this.querySelector(".id").innerText;
     window.location.href = `/course-details/${course_id}`;
  });
});