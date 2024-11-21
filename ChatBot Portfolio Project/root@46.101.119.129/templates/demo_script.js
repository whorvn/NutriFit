const questionText = document.querySelector(".title-text .question");
const questionForm = document.querySelector("form.question");
const questionBtn = document.querySelector("label.question");
const planBtn = document.querySelector("label.plan");

planBtn.onclick = () => {
  questionForm.style.marginLeft = "-50%";
  questionText.style.marginLeft = "-50%";
};

questionBtn.onclick = () => {
  questionForm.style.marginLeft = "0%";
  questionText.style.marginLeft = "0%";
};
