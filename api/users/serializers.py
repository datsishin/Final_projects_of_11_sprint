import base64import randomimport stringfrom base64 import encodefrom django.core.cache import cachefrom django.core.mail import send_mailfrom rest_framework import serializersfrom rest_framework.exceptions import ValidationErrorfrom rest_framework_simplejwt.serializers import TokenObtainPairSerializerfrom api.users.models import Userfrom api_yamdb import settingsdef encode(text):    enc_bytes = text.encode('ascii')    base64_bytes = base64.b64encode(enc_bytes)    base64_enc = base64_bytes.decode('ascii')    return base64_encdef decode(text):    base64_bytes = text.encode('ascii')    text_bytes = base64.b64decode(base64_bytes)    decoded_text = text_bytes.decode('ascii')    return decoded_textclass UserRegistrationSerializer(serializers.ModelSerializer):    class Meta:        model = User        fields = ('email',)    def create(self, validated_data):        email = validated_data['email']        if User.objects.filter(email=email).exists():            raise serializers.errors(ValidationError, {                'email': 'Пользователь с таким email уже зарегистрирован!'            })        confirmation_code = encode(            ''.join(random.choice(                string.ascii_uppercase + string.digits + string.ascii_lowercase            ) for _ in range(20))        )        username = email.replace('@', '_').replace('.', '_')        c_c = confirmation_code        cache.set_many({'u': username, 'e': email, 'c_c': c_c}, timeout=300)        send_mail(            'Confirmation code',            f'Ваш код подтверждения: {confirmation_code}',            settings.EMAIL_HOST_USER,            [email],            fail_silently=False,        )        return self.data['email']class MyAuthTokenSerializer(serializers.ModelSerializer):    email = serializers.EmailField()    class Meta:        model = User        fields = ('email', 'confirmation_code')    def validate(self, data):        # Берем из немодифицированных данных email (не понятно зачем) и код подтверждения просто из данных        send_email = self.initial_data['email']        send_confirmation_code = data['confirmation_code']        # Задаем словарь data с значениями из кэша (username, email, confirmation_code)        data = cache.get_many(['u', 'e', 'c_c'])        # Если кэш пустой        if not data:            raise serializers.ValidationError(                'Время подтверждения регистрации истекло'            )        # Вносим данные о пользователе из кэша        username = data['u']        email = data['e']        confirmation_code = data['c_c']        # Если код подтверждения первоначальный и присланный сходятся, то регистрируем пользователя        if send_confirmation_code == confirmation_code:            user = User.objects.create_user(                username=username,                email=email,                confirmation_code=confirmation_code,            )            user.save()            refresh = TokenObtainPairSerializer.get_token(user)            data['token'] = str(refresh.access_token)            return dataclass UserSerializer(serializers.ModelSerializer):    class Meta:        model = User        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )