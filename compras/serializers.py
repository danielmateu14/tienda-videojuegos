from rest_framework import serializers
from django.db import transaction
from .models import Compra
from juegos.models import Videojuego

class CompraSerializer(serializers.ModelSerializer):
    videojuego_titulo = serializers.CharField(source='videojuego.titulo', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = [
            'id', 'usuario', 'videojuego', 'videojuego_titulo',
            'cantidad', 'precio_unitario', 'total', 'fecha'
        ]
        read_only_fields = ['usuario', 'precio_unitario', 'fecha']

    def get_total(self, obj):
        return str(obj.total)

    def validate_cantidad(self, value):
        if value is None or int(value) <= 0:
            raise serializers.ValidationError('Debe ser mayor que 0.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        - Toma el precio actual del videojuego como precio_unitario.
        - Bloquea el registro del videojuego (FOR UPDATE) para evitar condiciones de carrera.
        - Valida stock suficiente y descuenta.
        """
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError('Autenticación requerida.')

        videojuego = validated_data['videojuego']
        cantidad = validated_data['cantidad']

        # Lock pesimista
        videojuego = Videojuego.objects.select_for_update().get(pk=videojuego.pk)

        if videojuego.stock <= 0:
            raise serializers.ValidationError({'videojuego': 'Sin stock.'})
        if cantidad > videojuego.stock:
            raise serializers.ValidationError({'cantidad': 'Stock insuficiente.'})

        validated_data['usuario'] = request.user
        validated_data['precio_unitario'] = videojuego.precio

        # Descontar stock
        videojuego.stock -= cantidad
        videojuego.save(update_fields=['stock'])

        return super().create(validated_data)
