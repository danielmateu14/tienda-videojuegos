from rest_framework import serializers
from .models import Videojuego, Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'videojuego', 'autor_nombre', 'texto', 'fecha_creacion']
        extra_kwargs = {
            'texto': {'required': True}
        }

    def get_autor_nombre(self, obj):
        extra = " (staff)" if obj.autor.rol in ['admin', 'empleado'] else ""
        return f"{obj.autor.username}{extra}"

    def validate_texto(self, value):
        if not value.strip():
            raise serializers.ValidationError("El comentario no puede estar vacío.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        videojuego = data.get('videojuego') or self.initial_data.get('videojuego')
        if request and request.user.is_authenticated and videojuego:
            ya_comento = Comentario.objects.filter(
                videojuego_id=videojuego,
                autor=request.user
            ).exists()
            if ya_comento:
                raise serializers.ValidationError("Ya has comentado este videojuego.")
        return data

class VideojuegoSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)  

    class Meta:
        model = Videojuego
        fields = ['id', 'titulo', 'descripcion', 'precio', 'stock', 'fecha_lanzamiento', 'comentarios']
