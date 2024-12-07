from utils.ultramsg import UltraMsgAPI

ultramsg = UltraMsgAPI()

# Send a text message
response_message = ultramsg.send_message(to='The-number', message='Hello, this is a test message!')
print(response_message.text)

# Send an image
response_image = ultramsg.send_image(
    to='The-number',
    image_url='https://blog.emania.com.br/wp-content/uploads/2016/02/direitos-autorais-e-de-imagem.jpg',
    caption='Test image'
)
print(response_image.text)