document.addEventListener("DOMContentLoaded", () => {
    const planContent = document.getElementById("plan-content");
    const chatContent = document.getElementById("chat-content");
    const switchToChat = document.getElementById("switch-to-chat");
    const switchToPlan = document.getElementById("switch-to-plan");

    switchToChat.addEventListener("click", () => {
        planContent.style.display = "none";
        chatContent.style.display = "flex";
    });

    switchToPlan.addEventListener("click", () => {
        chatContent.style.display = "none";
        planContent.style.display = "flex";
    });

    async function sendPersonalizedPlan(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const jsonData = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/personalized_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch. Server responded with status: ' + response.status);
            }

            const result = await response.json();
            alert('Personalized Plan Response: ' + JSON.stringify(result));
        } catch (error) {
            console.error('Error submitting Personalized Plan:', error);
            alert('Error: ' + error.message);
        }
    }

    async function sendQuestionAnswer(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const jsonData = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/question_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch. Server responded with status: ' + response.status);
            }

            const result = await response.json();
            const chatBox = document.getElementById("chat-box");
            const chatResponse = document.createElement("p");
            chatResponse.textContent = `NutriAI: ${result.response}`;
            chatBox.appendChild(chatResponse);
        } catch (error) {
            console.error('Error submitting Question Answer:', error);
            alert('Error: ' + error.message);
        }
    }

    document.getElementById("plan-form").addEventListener("submit", sendPersonalizedPlan);
    document.getElementById("chat-form").addEventListener("submit", sendQuestionAnswer);
});
