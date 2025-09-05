---
applyTo: '**'
---
# 🗂️ CONTEXTO DEL PROYECTO Y GUÍA DE CÓDIGO

Este documento define el propósito, las reglas y los estándares técnicos del proyecto. Eres un asistente experto en Flutter y debes adherirte estrictamente a estas directrices.

## 🎯 1. Objetivo Principal del Proyecto

* **Resumen**: Este archivo es una plantilla de contexto para acoplar a cualquier aplicación Flutter ya existente. Cuando utilices esta plantilla, debes escribir aquí un resumen personalizado del objetivo principal de tu aplicación. 
  
> **Instrucción:** Al agregar esta plantilla a tu proyecto, describe brevemente el propósito y funcionalidad principal de tu aplicación en este apartado. Todo el resto de las instrucciones y reglas se adaptarán a ese objetivo que definas aquí.
* **Tecnología Principal**: El proyecto está desarrollado en **Flutter**. Todas las soluciones deben ser específicas para este framework.

## 💻 2. Guía de Estilo y Código (Flutter/Dart)

* **Entorno y Dependencias**: Basa todo el código en las versiones de Flutter, Dart y las librerías definidas en el archivo `pubspec.yaml`. **No asumas versiones inexistentes en el proyecto**.
* **Logging**: **Usa siempre** el paquete `logger` para los registros de información. Está **prohibido** el uso de `print()`.
    * *Ejemplo de uso correcto:* `final logger = Logger(); logger.d('Mensaje de debug');`
* **Arquitectura y Principios S.O.L.I.D.**: El código debe ser limpio, mantenible y escalable.
    * Al generar o refactorizar, aplica activamente los principios **S.O.L.I.D.**
    * Cuando sugieras un cambio basado en estos principios, **explica brevemente qué principio estás aplicando** y por qué mejora el código.
* **Inmutabilidad**: Prefiere siempre objetos y colecciones inmutables cuando sea posible.
* **Formato y Estilo**: Sigue rigurosamente las convenciones de estilo de Dart (`effective_dart`). Usa `camelCase` para variables y funciones, y `PascalCase` para clases.
* **Idioma**: Todo el código, comentarios y documentación deben estar en **español**.