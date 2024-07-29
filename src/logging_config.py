import logging

def setup_logger():
    """
    Configura y devuelve un logger para la aplicación.

    Este logger registra mensajes en un archivo y en la consola con diferentes niveles de severidad y formatos.

    Returns:
        logger (logging.Logger): El logger configurado.
    """
    logger = logging.getLogger('loggs_scrap')
    logger.setLevel(logging.DEBUG)

    # Evita agregar manejadores múltiples
    if not logger.hasHandlers():
        # Crear un manejador de archivo que registra mensajes en 'loggs_scrap.log' con codificación UTF-8
        fh = logging.FileHandler('loggs_scrap.log', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Crear un manejador de consola que imprime mensajes de nivel ERROR y superior
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        
        # Definir el formato de los mensajes del log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Agregar los manejadores (archivo y consola) al logger
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger
