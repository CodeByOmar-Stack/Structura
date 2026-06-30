# 📝 Guía de Extensiones Personalizadas

## ¿Qué son las Extensiones Personalizadas?

Las extensiones personalizadas te permiten crear tus propias categorías de carpetas y asignar extensiones de archivo específicas a ellas. Esto es útil cuando tienes tipos de archivos que no están cubiertos por las categorías predefinidas.

### Ejemplo
Si trabajas frecuentemente con archivos de diseño como `.psd`, `.ai`, `.xd`, puedes crear una categoría llamada **"Diseño"** y asignarle estas extensiones. Cuando organices archivos, todos los archivos con estas extensiones se moverán automáticamente a la carpeta "Diseño".

---

## Cómo Usar

### Paso 1: Abrir el Administrador de Extensiones
1. Abre la aplicación GestorCarpetas
2. En el panel derecho, bajo "3. Opciones de Carpetas", haz clic en el botón **"📝 Extensiones Personalizadas"**
3. Se abrirá una ventana emergente titulada "Administrador de Extensiones Personalizadas"

### Paso 2: Crear una Nueva Categoría
1. En el campo **"Nombre de la carpeta"**, ingresa el nombre de tu categoría personalizada
   - Ejemplo: `Diseño`, `Proyectos`, `Desarrollos`
   - ⚠️ Evita caracteres especiales: `< > : " | ? *`

2. En el campo **"Extensiones"**, ingresa las extensiones separadas por comas
   - Ejemplo: `.psd, .ai, .xd`
   - ⚠️ Los puntos se agregan automáticamente, puedes escribir sin ellos
   - ⚠️ Separar con comas y espacios opcionales

3. Haz clic en **"➕ Agregar Categoría"** o presiona `Enter`

### Paso 3: Administrar Tus Categorías
- **Ver categorías**: Las categorías aparecen en el listado abajo
- **Eliminar una categoría**: Selecciona la categoría y haz clic en **"🗑️ Eliminar Seleccionada"**
- **Ver detalles**: Haz clic en una categoría para ver sus extensiones

### Paso 4: Cerrar y Guardar
- Haz clic en **"Cerrar"** para guardar y cerrar la ventana
- Las cambios se guardan automáticamente

---

## Ubicación de los Datos

Los datos de tus extensiones personalizadas se guardan en:
```
~/.gestor_carpetas/custom_extensions.json
```

**Ubicaciones por sistema operativo:**
- **Windows**: `C:\Users\TuUsuario\.gestor_carpetas\custom_extensions.json`
- **Linux/Mac**: `/home/TuUsuario/.gestor_carpetas/custom_extensions.json`

---

## Ejemplos Prácticos

### Ejemplo 1: Fotógrafo
```
Categoría: Fotos_RAW
Extensiones: .cr2, .nef, .arw, .raw

Categoría: Fotos_Editadas
Extensiones: .psd, .tiff, .jpg
```

### Ejemplo 2: Desarrollador
```
Categoría: Configuración
Extensiones: .json, .yaml, .yml, .ini, .conf

Categoría: Build
Extensiones: .o, .a, .so, .dll
```

### Ejemplo 3: Artista 3D
```
Categoría: Modelos_3D
Extensiones: .blend, .fbx, .obj, .maya

Categoría: Texturas
Extensiones: .exr, .tga, .hdr, .psd
```

---

## ¿Cómo Funciona la Organización?

1. **Al organizar archivos**, el sistema busca cada extensión en las categorías (primero predefinidas, luego personalizadas)
2. **Si encuentra una coincidencia**, mueve el archivo a esa carpeta
3. **Si no encuentra coincidencia**, mueve el archivo a la carpeta "Otros"

### Orden de Prioridad
1. Extensiones predefinidas (Imágenes, Documentos, Videos, etc.)
2. Extensiones personalizadas (en el orden que las creaste)
3. Si no hay coincidencia → Carpeta "Otros"

---

## Preguntas Frecuentes

### P: ¿Puedo editar una extensión existente?
**R:** Actualmente no. Elimina la categoría antigua y crea una nueva. Mejoras futuras permitirán editar directamente.

### P: ¿Puedo usar extensiones personalizadas con presets?
**R:** Sí. Las extensiones personalizadas se integran automáticamente con todos los presets. Si creas un preset, tus categorías personalizadas estarán disponibles.

### P: ¿Se pierden mis extensiones si desinstalo la app?
**R:** No. Los datos se guardan en tu carpeta de usuario (`~/.gestor_carpetas/`), así que persisten incluso después de desinstalar.

### P: ¿Puedo tener dos categorías con la misma extensión?
**R:** La última categoría agregada ganará. Es recomendable usar extensiones únicas por categoría.

### P: ¿Hay límite de categorías o extensiones?
**R:** No hay límite técnico, pero demasiadas pueden ralentizar la búsqueda. Se recomienda no más de 50-100 extensiones totales.

---

## Solución de Problemas

### Problema: Mi categoría no aparece en la lista
**Solución**: Asegúrate de haber ingresado correctamente el nombre y al menos una extensión.

### Problema: Los archivos no se están organizando en mi categoría personalizada
**Solución**: 
1. Verifica que las extensiones sean exactas (incluye el punto si es necesario)
2. Comprueba que la extensión no esté asignada a una categoría predefinida
3. Cierra y reabre la aplicación para recargar las extensiones

### Problema: Caracteres especiales no permitidos
**Evita estos caracteres en nombres de categoría:**
```
< > : " | ? * \ /
```
Usa solo letras, números, guiones y espacios.

---

## Próximas Mejoras Planeadas

- [ ] Editar categorías existentes directamente
- [ ] Importar/Exportar configuraciones
- [ ] Asignar iconos personalizados a categorías
- [ ] Crear conjuntos de extensiones (macros)
- [ ] Sincronizar entre dispositivos

---

¡Diviértete organizando tus archivos con categorías personalizadas! 🚀
