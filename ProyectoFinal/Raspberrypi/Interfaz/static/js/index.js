const { createApp, ref } = Vue;

const app = createApp({
    setup() {
        const ledStatus = ref('off');
        const imageData = ref('');

        const updateLedStatus = async () => {
            try {
                const response = await fetch('/update_led', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ ledStatus: ledStatus.value })
                });

                const data = await response.json();
                console.log(data);

            } catch (error) {
                console.error('Error:', error);
            }
        };

        const capturarFoto = async () => {
            try {
                const response = await fetch('/capture', {
                    method: 'POST'
                });

                const data = await response.json();
                console.log(data.response);
                imageData.value = data.response;

            } catch (error) {
                console.error('Error de red:', error);
            }
        };

        return { ledStatus, updateLedStatus, capturarFoto, imageData };
    },
    watch: {
        ledStatus(newValue, oldValue) {
            this.updateLedStatus();
        }
    }
});

app.mount('#app');
