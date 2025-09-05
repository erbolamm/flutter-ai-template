# Instrucciones Modulares para Agentes AI

Este directorio contiene los módulos de reglas consumidos por el índice maestro `../copilot-instructions.md`.

## Archivos
- `contexto.instructions.md`: Objetivo del proyecto, estilo de código, SOLID, logging.
- `iteraccion.instructions.md`: Filosofía de interacción, tono, confirmación 1/2/3, pensamiento crítico.

## Principios
1. Fuente única de verdad: modificaciones conceptuales se aplican aquí y el índice solo resume.
2. No duplicar texto extenso en el índice maestro.
3. Mantener español consistente y ejemplos concretos.
4. Cada nuevo ámbito (ej. manejo de errores detallado, pipeline audio) debe añadirse como `*.instructions.md` y enlazarse.

## Cómo ampliar
1. Crear archivo `nuevo_tema.instructions.md`.
2. Añadir sección clara con encabezados (`##`).
3. Referenciarlo en la tabla del índice maestro.
4. Evitar introducir reglas que contradigan archivos existentes; si hay conflicto, refactorizar.

## Mantenimiento Rápido
- Revisar tras cambios en `pubspec.yaml` para dependencias nuevas.
- Eliminar reglas obsoletas (ej. libs retiradas).
- Validar que ejemplos de rutas de archivos existan realmente.

---
Última actualización: automatizada.
