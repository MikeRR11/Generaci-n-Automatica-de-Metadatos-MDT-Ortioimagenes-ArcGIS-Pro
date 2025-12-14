# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Script: GENERACION DE METADATOS PARA TERCEROS SEGUN ISO 19139
# Elaboró / Modificó: MICHAEL ANDRES ROJAS RIVERA - YARITZA DORELY QUEVEDO TOVAR
# -----------------------------------------------------------------------------
'''
Descripción:
Este script automatiza la generación de metadatos para MDT y Ortoimagenes utilizando
la librería ArcPy y estándares internacionales de metadatos geográficos (ISO 19115).
Incluye configuraciones específicas de la organización y palabras clave
relacionadas con temas geoespaciales, exportación en formato XML, creación de thumbnail
y la generación de PDF del metadato.

# Uso:
- Asegúrese de tener ArcGIS instalado y configurado correctamente.
- Ejecute el script en un entorno compatible con Python y ArcPy
#
# Dependencias:
- Python 3.x
- ArcPy


# Notas:
- Este script utiliza namespaces definidos por ISO 19115 para la manipulación
  de metadatos en formato XML.
- Personalice las constantes de la organización y palabras clave según sea necesario.

# Fecha creación: 02/05/2025
# Última Modificación: 05/11/2025
# -----------------------------------------------------------------------------
'''
#Importacion de librerias 
import arcpy
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import random
import uuid
import math
from arcpy import metadata as md
import traceback
import tempfile
from typing import List, Dict, Set
import platform
import unicodedata



# =============================================
# CONSTANTES Y CONFIGURACIONES
# =============================================

# Definición global de namespaces
NSMAP = {
    None: 'http://www.isotc211.org/2005/gmd',
    'gco': 'http://www.isotc211.org/2005/gco',
    'gts': 'http://www.isotc211.org/2005/gts',
    'srv': 'http://www.isotc211.org/2005/srv',
    'gml': 'http://www.opengis.net/gml/3.2',
    'gmx': 'http://www.isotc211.org/2005/gmx',
    'xlink': 'http://www.w3.org/1999/xlink',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}


# Keywords predefinidas (MDT)
MDT_KEYWORDS = {
    'temas': ['Modelo Digital de Terreno', 'MDT', 'Topografía', 'Cartografía Básica'],
    'categorias': [
        'geoscientificInformation',
        'environment',
        'imageryBaseMapsEarthCover',
        'elevation',
        'boundaries',
        'location',
        'planningCadastre'
    ]
}

# Keywords predefinidas (ORTOIMAGENES)
ORTO_KEYWORDS = {
    'temas': ['Ortoimagen', 'Ortofotomosaico', 'Ortofoto', 'Mosaico'],
    'categorias': [
        'geoscientificInformation',
        'environment',
        'transportation',
        'imageryBaseMapsEarthCover',
        'intelligenceMilitary',
        'location',
        'planningCadastre'
    ]
}


# Diccionario de referencia para datos geográficos
dane_dict = {
    "05": {
        "Departamento": "DE ANTIOQUIA"
    },
    "08": {
        "Departamento": "DEL ATLÁNTICO"
    },
    "11": {
        "Departamento": "DE BOGOTÁ D.C."
    },
    "13": {
        "Departamento": "DE BOLÍVAR"
    },
    "15": {
        "Departamento": "DE BOYACÁ"
    },
    "17": {
        "Departamento": "DE CALDAS"
    },
    "18": {
        "Departamento": "DE CAQUETÁ"
    },
    "19": {
        "Departamento": "DEL CAUCA"
    },
    "20": {
        "Departamento": "DEL CESAR"
    },
    "23": {
        "Departamento": "DE CÓRDOBA"
    },
    "25": {
        "Departamento": "DE CUNDINAMARCA"
    },
    "27": {
        "Departamento": "DEL CHOCÓ"
    },
    "41": {
        "Departamento": "DEL HUILA"
    },
    "44": {
        "Departamento": "DE LA GUAJIRA"
    },
    "47": {
        "Departamento": "DEL MAGDALENA"
    },
    "50": {
        "Departamento": "DEL META"
    },
    "52": {
        "Departamento": "DE NARIÑO"
    },
    "54": {
        "Departamento": "DE NORTE DE SANTANDER"
    },
    "63": {
        "Departamento": "DEL QUINDÍO"
    },
    "66": {
        "Departamento": "DE RISARALDA"
    },
    "68": {
        "Departamento": "DE SANTANDER"
    },
    "70": {
        "Departamento": "DE SUCRE"
    },
    "73": {
        "Departamento": "DEL TOLIMA"
    },
    "76": {
        "Departamento": "DEL VALLE DEL CAUCA"
    },
    "81": {
        "Departamento": "DE ARAUCA"
    },
    "85": {
        "Departamento": "DE CASANARE"
    },
    "86": {
        "Departamento": "DEL PUTUMAYO"
    },
    "88": {
        "Departamento": "DE ARCHIPIÉLAGO DE SAN ANDRÉS PROVIDENCIA Y SANTA CATALINA"
    },
    "91": {
        "Departamento": "DEL AMAZONAS"
    },
    "94": {
        "Departamento": "DE GUAINÍA"
    },
    "95": {
        "Departamento": "DEL GUAVIARE"
    },
    "97": {
        "Departamento": "DEL VAUPÉS"
    },
    "99": {
        "Departamento": "DEL VICHADA"
    },
    "05001": {
        "Municipio": "MEDELLÍN"
    },
    "05002": {
        "Municipio": "ABEJORRAL"
    },
    "05004": {
        "Municipio": "ABRIAQUÍ"
    },
    "05021": {
        "Municipio": "ALEJANDRÍA"
    },
    "05030": {
        "Municipio": "AMAGÁ"
    },
    "05031": {
        "Municipio": "AMALFI"
    },
    "05034": {
        "Municipio": "ANDES"
    },
    "05036": {
        "Municipio": "ANGELÓPOLIS"
    },
    "05038": {
        "Municipio": "ANGOSTURA"
    },
    "05040": {
        "Municipio": "ANORÍ"
    },
    "05042": {
        "Municipio": "SANTA FÉ DE ANTIOQUIA"
    },
    "05044": {
        "Municipio": "ANZÁ"
    },
    "05045": {
        "Municipio": "APARTADÓ"
    },
    "05051": {
        "Municipio": "ARBOLETES"
    },
    "05055": {
        "Municipio": "ARGELIA"
    },
    "05059": {
        "Municipio": "ARMENIA"
    },
    "05079": {
        "Municipio": "BARBOSA"
    },
    "05086": {
        "Municipio": "BELMIRA"
    },
    "05088": {
        "Municipio": "BELLO"
    },
    "05091": {
        "Municipio": "BETANIA"
    },
    "05093": {
        "Municipio": "BETULIA"
    },
    "05101": {
        "Municipio": "CIUDAD BOLÍVAR"
    },
    "05107": {
        "Municipio": "BRICEÑO"
    },
    "05113": {
        "Municipio": "BURITICÁ"
    },
    "05120": {
        "Municipio": "CÁCERES"
    },
    "05125": {
        "Municipio": "CAICEDO"
    },
    "05129": {
        "Municipio": "CALDAS"
    },
    "05134": {
        "Municipio": "CAMPAMENTO"
    },
    "05138": {
        "Municipio": "CAÑASGORDAS"
    },
    "05142": {
        "Municipio": "CARACOLÍ"
    },
    "05145": {
        "Municipio": "CARAMANTA"
    },
    "05147": {
        "Municipio": "CAREPA"
    },
    "05148": {
        "Municipio": "EL CARMEN DE VIBORAL"
    },
    "05150": {
        "Municipio": "CAROLINA"
    },
    "05154": {
        "Municipio": "CAUCASIA"
    },
    "05172": {
        "Municipio": "CHIGORODÓ"
    },
    "05190": {
        "Municipio": "CISNEROS"
    },
    "05197": {
        "Municipio": "COCORNÁ"
    },
    "05206": {
        "Municipio": "CONCEPCIÓN"
    },
    "05209": {
        "Municipio": "CONCORDIA"
    },
    "05212": {
        "Municipio": "COPACABANA"
    },
    "05234": {
        "Municipio": "DABEIBA"
    },
    "05237": {
        "Municipio": "DONMATÍAS"
    },
    "05240": {
        "Municipio": "EBÉJICO"
    },
    "05250": {
        "Municipio": "EL BAGRE"
    },
    "05264": {
        "Municipio": "ENTRERRÍOS"
    },
    "05266": {
        "Municipio": "ENVIGADO"
    },
    "05282": {
        "Municipio": "FREDONIA"
    },
    "05284": {
        "Municipio": "FRONTINO"
    },
    "05306": {
        "Municipio": "GIRALDO"
    },
    "05308": {
        "Municipio": "GIRARDOTA"
    },
    "05310": {
        "Municipio": "GÓMEZ PLATA"
    },
    "05313": {
        "Municipio": "GRANADA"
    },
    "05315": {
        "Municipio": "GUADALUPE"
    },
    "05318": {
        "Municipio": "GUARNE"
    },
    "05321": {
        "Municipio": "GUATAPÉ"
    },
    "05347": {
        "Municipio": "HELICONIA"
    },
    "05353": {
        "Municipio": "HISPANIA"
    },
    "05360": {
        "Municipio": "ITAGÜÍ"
    },
    "05361": {
        "Municipio": "ITUANGO"
    },
    "05364": {
        "Municipio": "JARDÍN"
    },
    "05368": {
        "Municipio": "JERICÓ"
    },
    "05376": {
        "Municipio": "LA CEJA"
    },
    "05380": {
        "Municipio": "LA ESTRELLA"
    },
    "05390": {
        "Municipio": "LA PINTADA"
    },
    "05400": {
        "Municipio": "LA UNIÓN"
    },
    "05411": {
        "Municipio": "LIBORINA"
    },
    "05425": {
        "Municipio": "MACEO"
    },
    "05440": {
        "Municipio": "MARINILLA"
    },
    "05467": {
        "Municipio": "MONTEBELLO"
    },
    "05475": {
        "Municipio": "MURINDÓ"
    },
    "05480": {
        "Municipio": "MUTATÁ"
    },
    "05483": {
        "Municipio": "NARIÑO"
    },
    "05490": {
        "Municipio": "NECOCLÍ"
    },
    "05495": {
        "Municipio": "NECHÍ"
    },
    "05501": {
        "Municipio": "OLAYA"
    },
    "05541": {
        "Municipio": "PEÑOL"
    },
    "05543": {
        "Municipio": "PEQUE"
    },
    "05576": {
        "Municipio": "PUEBLORRICO"
    },
    "05579": {
        "Municipio": "PUERTO BERRÍO"
    },
    "05585": {
        "Municipio": "PUERTO NARE"
    },
    "05591": {
        "Municipio": "PUERTO TRIUNFO"
    },
    "05604": {
        "Municipio": "REMEDIOS"
    },
    "05607": {
        "Municipio": "RETIRO"
    },
    "05615": {
        "Municipio": "RIONEGRO"
    },
    "05628": {
        "Municipio": "SABANALARGA"
    },
    "05631": {
        "Municipio": "SABANETA"
    },
    "05642": {
        "Municipio": "SALGAR"
    },
    "05647": {
        "Municipio": "SAN ANDRÉS DE CUERQUÍA"
    },
    "05649": {
        "Municipio": "SAN CARLOS"
    },
    "05652": {
        "Municipio": "SAN FRANCISCO"
    },
    "05656": {
        "Municipio": "SAN JERÓNIMO"
    },
    "05658": {
        "Municipio": "SAN JOSÉ DE LA MONTAÑA"
    },
    "05659": {
        "Municipio": "SAN JUAN DE URABÁ"
    },
    "05660": {
        "Municipio": "SAN LUIS"
    },
    "05664": {
        "Municipio": "SAN PEDRO DE LOS MILAGROS"
    },
    "05665": {
        "Municipio": "SAN PEDRO DE URABÁ"
    },
    "05667": {
        "Municipio": "SAN RAFAEL"
    },
    "05670": {
        "Municipio": "SAN ROQUE"
    },
    "05674": {
        "Municipio": "SAN VICENTE FERRER"
    },
    "05679": {
        "Municipio": "SANTA BÁRBARA"
    },
    "05686": {
        "Municipio": "SANTA ROSA DE OSOS"
    },
    "05690": {
        "Municipio": "SANTO DOMINGO"
    },
    "05697": {
        "Municipio": "EL SANTUARIO"
    },
    "05736": {
        "Municipio": "SEGOVIA"
    },
    "05756": {
        "Municipio": "SONSÓN"
    },
    "05761": {
        "Municipio": "SOPETRÁN"
    },
    "05789": {
        "Municipio": "TÁMESIS"
    },
    "05790": {
        "Municipio": "TARAZÁ"
    },
    "05792": {
        "Municipio": "TARSO"
    },
    "05809": {
        "Municipio": "TITIRIBÍ"
    },
    "05819": {
        "Municipio": "TOLEDO"
    },
    "05837": {
        "Municipio": "TURBO"
    },
    "05842": {
        "Municipio": "URAMITA"
    },
    "05847": {
        "Municipio": "URRAO"
    },
    "05854": {
        "Municipio": "VALDIVIA"
    },
    "05856": {
        "Municipio": "VALPARAÍSO"
    },
    "05858": {
        "Municipio": "VEGACHÍ"
    },
    "05861": {
        "Municipio": "VENECIA"
    },
    "05873": {
        "Municipio": "VIGÍA DEL FUERTE"
    },
    "05885": {
        "Municipio": "YALÍ"
    },
    "05887": {
        "Municipio": "YARUMAL"
    },
    "05890": {
        "Municipio": "YOLOMBÓ"
    },
    "05893": {
        "Municipio": "YONDÓ"
    },
    "05895": {
        "Municipio": "ZARAGOZA"
    },
    "08001": {
        "Municipio": "BARRANQUILLA"
    },
    "08078": {
        "Municipio": "BARANOA"
    },
    "08137": {
        "Municipio": "CAMPO DE LA CRUZ"
    },
    "08141": {
        "Municipio": "CANDELARIA"
    },
    "08296": {
        "Municipio": "GALAPA"
    },
    "08372": {
        "Municipio": "JUAN DE ACOSTA"
    },
    "08421": {
        "Municipio": "LURUACO"
    },
    "08433": {
        "Municipio": "MALAMBO"
    },
    "08436": {
        "Municipio": "MANATÍ"
    },
    "08520": {
        "Municipio": "PALMAR DE VARELA"
    },
    "08549": {
        "Municipio": "PIOJÓ"
    },
    "08558": {
        "Municipio": "POLONUEVO"
    },
    "08560": {
        "Municipio": "PONEDERA"
    },
    "08573": {
        "Municipio": "PUERTO COLOMBIA"
    },
    "08606": {
        "Municipio": "REPELÓN"
    },
    "08634": {
        "Municipio": "SABANAGRANDE"
    },
    "08638": {
        "Municipio": "SABANALARGA"
    },
    "08675": {
        "Municipio": "SANTA LUCÍA"
    },
    "08685": {
        "Municipio": "SANTO TOMÁS"
    },
    "08758": {
        "Municipio": "SOLEDAD"
    },
    "08770": {
        "Municipio": "SUAN"
    },
    "08832": {
        "Municipio": "TUBARÁ"
    },
    "08849": {
        "Municipio": "USIACURÍ"
    },
    "11001": {
        "Municipio": "BOGOTÁ D.C."
    },
    "13001": {
        "Municipio": "CARTAGENA DE INDIAS"
    },
    "13006": {
        "Municipio": "ACHÍ"
    },
    "13030": {
        "Municipio": "ALTOS DEL ROSARIO"
    },
    "13042": {
        "Municipio": "ARENAL"
    },
    "13052": {
        "Municipio": "ARJONA"
    },
    "13062": {
        "Municipio": "ARROYOHONDO"
    },
    "13074": {
        "Municipio": "BARRANCO DE LOBA"
    },
    "13140": {
        "Municipio": "CALAMAR"
    },
    "13160": {
        "Municipio": "CANTAGALLO"
    },
    "13188": {
        "Municipio": "CICUCO"
    },
    "13212": {
        "Municipio": "CÓRDOBA"
    },
    "13222": {
        "Municipio": "CLEMENCIA"
    },
    "13244": {
        "Municipio": "EL CARMEN DE BOLÍVAR"
    },
    "13248": {
        "Municipio": "EL GUAMO"
    },
    "13268": {
        "Municipio": "EL PEÑÓN"
    },
    "13300": {
        "Municipio": "HATILLO DE LOBA"
    },
    "13430": {
        "Municipio": "MAGANGUÉ"
    },
    "13433": {
        "Municipio": "MAHATES"
    },
    "13440": {
        "Municipio": "MARGARITA"
    },
    "13442": {
        "Municipio": "MARÍA LA BAJA"
    },
    "13458": {
        "Municipio": "MONTECRISTO"
    },
    "13468": {
        "Municipio": "SANTA CRUZ DE MOMPOX"
    },
    "13473": {
        "Municipio": "MORALES"
    },
    "13490": {
        "Municipio": "NOROSÍ"
    },
    "13549": {
        "Municipio": "PINILLOS"
    },
    "13580": {
        "Municipio": "REGIDOR"
    },
    "13600": {
        "Municipio": "RÍO VIEJO"
    },
    "13620": {
        "Municipio": "SAN CRISTÓBAL"
    },
    "13647": {
        "Municipio": "SAN ESTANISLAO"
    },
    "13650": {
        "Municipio": "SAN FERNANDO"
    },
    "13654": {
        "Municipio": "SAN JACINTO"
    },
    "13655": {
        "Municipio": "SAN JACINTO DEL CAUCA"
    },
    "13657": {
        "Municipio": "SAN JUAN NEPOMUCENO"
    },
    "13667": {
        "Municipio": "SAN MARTÍN DE LOBA"
    },
    "13670": {
        "Municipio": "SAN PABLO"
    },
    "13673": {
        "Municipio": "SANTA CATALINA"
    },
    "13683": {
        "Municipio": "SANTA ROSA"
    },
    "13688": {
        "Municipio": "SANTA ROSA DEL SUR"
    },
    "13744": {
        "Municipio": "SIMITÍ"
    },
    "13760": {
        "Municipio": "SOPLAVIENTO"
    },
    "13780": {
        "Municipio": "TALAIGUA NUEVO"
    },
    "13810": {
        "Municipio": "TIQUISIO"
    },
    "13836": {
        "Municipio": "TURBACO"
    },
    "13838": {
        "Municipio": "TURBANÁ"
    },
    "13873": {
        "Municipio": "VILLANUEVA"
    },
    "13894": {
        "Municipio": "ZAMBRANO"
    },
    "15001": {
        "Municipio": "TUNJA"
    },
    "15022": {
        "Municipio": "ALMEIDA"
    },
    "15047": {
        "Municipio": "AQUITANIA"
    },
    "15051": {
        "Municipio": "ARCABUCO"
    },
    "15087": {
        "Municipio": "BELÉN"
    },
    "15090": {
        "Municipio": "BERBEO"
    },
    "15092": {
        "Municipio": "BETÉITIVA"
    },
    "15097": {
        "Municipio": "BOAVITA"
    },
    "15104": {
        "Municipio": "BOYACÁ"
    },
    "15106": {
        "Municipio": "BRICEÑO"
    },
    "15109": {
        "Municipio": "BUENAVISTA"
    },
    "15114": {
        "Municipio": "BUSBANZÁ"
    },
    "15131": {
        "Municipio": "CALDAS"
    },
    "15135": {
        "Municipio": "CAMPOHERMOSO"
    },
    "15162": {
        "Municipio": "CERINZA"
    },
    "15172": {
        "Municipio": "CHINAVITA"
    },
    "15176": {
        "Municipio": "CHIQUINQUIRÁ"
    },
    "15180": {
        "Municipio": "CHISCAS"
    },
    "15183": {
        "Municipio": "CHITA"
    },
    "15185": {
        "Municipio": "CHITARAQUE"
    },
    "15187": {
        "Municipio": "CHIVATÁ"
    },
    "15189": {
        "Municipio": "CIÉNEGA"
    },
    "15204": {
        "Municipio": "CÓMBITA"
    },
    "15212": {
        "Municipio": "COPER"
    },
    "15215": {
        "Municipio": "CORRALES"
    },
    "15218": {
        "Municipio": "COVARACHÍA"
    },
    "15223": {
        "Municipio": "CUBARÁ"
    },
    "15224": {
        "Municipio": "CUCAITA"
    },
    "15226": {
        "Municipio": "CUÍTIVA"
    },
    "15232": {
        "Municipio": "CHÍQUIZA"
    },
    "15236": {
        "Municipio": "CHIVOR"
    },
    "15238": {
        "Municipio": "DUITAMA"
    },
    "15244": {
        "Municipio": "EL COCUY"
    },
    "15248": {
        "Municipio": "EL ESPINO"
    },
    "15272": {
        "Municipio": "FIRAVITOBA"
    },
    "15276": {
        "Municipio": "FLORESTA"
    },
    "15293": {
        "Municipio": "GACHANTIVÁ"
    },
    "15296": {
        "Municipio": "GÁMEZA"
    },
    "15299": {
        "Municipio": "GARAGOA"
    },
    "15317": {
        "Municipio": "GUACAMAYAS"
    },
    "15322": {
        "Municipio": "GUATEQUE"
    },
    "15325": {
        "Municipio": "GUAYATÁ"
    },
    "15332": {
        "Municipio": "GÜICÁN DE LA SIERRA"
    },
    "15362": {
        "Municipio": "IZA"
    },
    "15367": {
        "Municipio": "JENESANO"
    },
    "15368": {
        "Municipio": "JERICÓ"
    },
    "15377": {
        "Municipio": "LABRANZAGRANDE"
    },
    "15380": {
        "Municipio": "LA CAPILLA"
    },
    "15401": {
        "Municipio": "LA VICTORIA"
    },
    "15403": {
        "Municipio": "LA UVITA"
    },
    "15407": {
        "Municipio": "VILLA DE LEYVA"
    },
    "15425": {
        "Municipio": "MACANAL"
    },
    "15442": {
        "Municipio": "MARIPÍ"
    },
    "15455": {
        "Municipio": "MIRAFLORES"
    },
    "15464": {
        "Municipio": "MONGUA"
    },
    "15466": {
        "Municipio": "MONGUÍ"
    },
    "15469": {
        "Municipio": "MONIQUIRÁ"
    },
    "15476": {
        "Municipio": "MOTAVITA"
    },
    "15480": {
        "Municipio": "MUZO"
    },
    "15491": {
        "Municipio": "NOBSA"
    },
    "15494": {
        "Municipio": "NUEVO COLÓN"
    },
    "15500": {
        "Municipio": "OICATÁ"
    },
    "15507": {
        "Municipio": "OTANCHE"
    },
    "15511": {
        "Municipio": "PACHAVITA"
    },
    "15514": {
        "Municipio": "PÁEZ"
    },
    "15516": {
        "Municipio": "PAIPA"
    },
    "15518": {
        "Municipio": "PAJARITO"
    },
    "15522": {
        "Municipio": "PANQUEBA"
    },
    "15531": {
        "Municipio": "PAUNA"
    },
    "15533": {
        "Municipio": "PAYA"
    },
    "15537": {
        "Municipio": "PAZ DE RÍO"
    },
    "15542": {
        "Municipio": "PESCA"
    },
    "15550": {
        "Municipio": "PISBA"
    },
    "15572": {
        "Municipio": "PUERTO BOYACÁ"
    },
    "15580": {
        "Municipio": "QUÍPAMA"
    },
    "15599": {
        "Municipio": "RAMIRIQUÍ"
    },
    "15600": {
        "Municipio": "RÁQUIRA"
    },
    "15621": {
        "Municipio": "RONDÓN"
    },
    "15632": {
        "Municipio": "SABOYÁ"
    },
    "15638": {
        "Municipio": "SÁCHICA"
    },
    "15646": {
        "Municipio": "SAMACÁ"
    },
    "15660": {
        "Municipio": "SAN EDUARDO"
    },
    "15664": {
        "Municipio": "SAN JOSÉ DE PARE"
    },
    "15667": {
        "Municipio": "SAN LUIS DE GACENO"
    },
    "15673": {
        "Municipio": "SAN MATEO"
    },
    "15676": {
        "Municipio": "SAN MIGUEL DE SEMA"
    },
    "15681": {
        "Municipio": "SAN PABLO DE BORBUR"
    },
    "15686": {
        "Municipio": "SANTANA"
    },
    "15690": {
        "Municipio": "SANTA MARÍA"
    },
    "15693": {
        "Municipio": "SANTA ROSA DE VITERBO"
    },
    "15696": {
        "Municipio": "SANTA SOFÍA"
    },
    "15720": {
        "Municipio": "SATIVANORTE"
    },
    "15723": {
        "Municipio": "SATIVASUR"
    },
    "15740": {
        "Municipio": "SIACHOQUE"
    },
    "15753": {
        "Municipio": "SOATÁ"
    },
    "15755": {
        "Municipio": "SOCOTÁ"
    },
    "15757": {
        "Municipio": "SOCHA"
    },
    "15759": {
        "Municipio": "SOGAMOSO"
    },
    "15761": {
        "Municipio": "SOMONDOCO"
    },
    "15762": {
        "Municipio": "SORA"
    },
    "15763": {
        "Municipio": "SOTAQUIRÁ"
    },
    "15764": {
        "Municipio": "SORACÁ"
    },
    "15774": {
        "Municipio": "SUSACÓN"
    },
    "15776": {
        "Municipio": "SUTAMARCHÁN"
    },
    "15778": {
        "Municipio": "SUTATENZA"
    },
    "15790": {
        "Municipio": "TASCO"
    },
    "15798": {
        "Municipio": "TENZA"
    },
    "15804": {
        "Municipio": "TIBANÁ"
    },
    "15806": {
        "Municipio": "TIBASOSA"
    },
    "15808": {
        "Municipio": "TINJACÁ"
    },
    "15810": {
        "Municipio": "TIPACOQUE"
    },
    "15814": {
        "Municipio": "TOCA"
    },
    "15816": {
        "Municipio": "TOGÜÍ"
    },
    "15820": {
        "Municipio": "TÓPAGA"
    },
    "15822": {
        "Municipio": "TOTA"
    },
    "15832": {
        "Municipio": "TUNUNGUÁ"
    },
    "15835": {
        "Municipio": "TURMEQUÉ"
    },
    "15837": {
        "Municipio": "TUTA"
    },
    "15839": {
        "Municipio": "TUTAZÁ"
    },
    "15842": {
        "Municipio": "ÚMBITA"
    },
    "15861": {
        "Municipio": "VENTAQUEMADA"
    },
    "15879": {
        "Municipio": "VIRACACHÁ"
    },
    "15897": {
        "Municipio": "ZETAQUIRA"
    },
    "17001": {
        "Municipio": "MANIZALES"
    },
    "17013": {
        "Municipio": "AGUADAS"
    },
    "17042": {
        "Municipio": "ANSERMA"
    },
    "17050": {
        "Municipio": "ARANZAZU"
    },
    "17088": {
        "Municipio": "BELALCÁZAR"
    },
    "17174": {
        "Municipio": "CHINCHINÁ"
    },
    "17272": {
        "Municipio": "FILADELFIA"
    },
    "17380": {
        "Municipio": "LA DORADA"
    },
    "17388": {
        "Municipio": "LA MERCED"
    },
    "17433": {
        "Municipio": "MANZANARES"
    },
    "17442": {
        "Municipio": "MARMATO"
    },
    "17444": {
        "Municipio": "MARQUETALIA"
    },
    "17446": {
        "Municipio": "MARULANDA"
    },
    "17486": {
        "Municipio": "NEIRA"
    },
    "17495": {
        "Municipio": "NORCASIA"
    },
    "17513": {
        "Municipio": "PÁCORA"
    },
    "17524": {
        "Municipio": "PALESTINA"
    },
    "17541": {
        "Municipio": "PENSILVANIA"
    },
    "17614": {
        "Municipio": "RIOSUCIO"
    },
    "17616": {
        "Municipio": "RISARALDA"
    },
    "17653": {
        "Municipio": "SALAMINA"
    },
    "17662": {
        "Municipio": "SAMANÁ"
    },
    "17665": {
        "Municipio": "SAN JOSÉ"
    },
    "17777": {
        "Municipio": "SUPÍA"
    },
    "17867": {
        "Municipio": "VICTORIA"
    },
    "17873": {
        "Municipio": "VILLAMARÍA"
    },
    "17877": {
        "Municipio": "VITERBO"
    },
    "18001": {
        "Municipio": "FLORENCIA"
    },
    "18029": {
        "Municipio": "ALBANIA"
    },
    "18094": {
        "Municipio": "BELÉN DE LOS ANDAQUÍES"
    },
    "18150": {
        "Municipio": "CARTAGENA DEL CHAIRÁ"
    },
    "18205": {
        "Municipio": "CURILLO"
    },
    "18247": {
        "Municipio": "EL DONCELLO"
    },
    "18256": {
        "Municipio": "EL PAUJÍL"
    },
    "18410": {
        "Municipio": "LA MONTAÑITA"
    },
    "18460": {
        "Municipio": "MILÁN"
    },
    "18479": {
        "Municipio": "MORELIA"
    },
    "18592": {
        "Municipio": "PUERTO RICO"
    },
    "18610": {
        "Municipio": "SAN JOSÉ DEL FRAGUA"
    },
    "18753": {
        "Municipio": "SAN VICENTE DEL CAGUÁN"
    },
    "18756": {
        "Municipio": "SOLANO"
    },
    "18785": {
        "Municipio": "SOLITA"
    },
    "18860": {
        "Municipio": "VALPARAÍSO"
    },
    "19001": {
        "Municipio": "POPAYÁN"
    },
    "19022": {
        "Municipio": "ALMAGUER"
    },
    "19050": {
        "Municipio": "ARGELIA"
    },
    "19075": {
        "Municipio": "BALBOA"
    },
    "19100": {
        "Municipio": "BOLÍVAR"
    },
    "19110": {
        "Municipio": "BUENOS AIRES"
    },
    "19130": {
        "Municipio": "CAJIBÍO"
    },
    "19137": {
        "Municipio": "CALDONO"
    },
    "19142": {
        "Municipio": "CALOTO"
    },
    "19212": {
        "Municipio": "CORINTO"
    },
    "19256": {
        "Municipio": "EL TAMBO"
    },
    "19290": {
        "Municipio": "FLORENCIA"
    },
    "19300": {
        "Municipio": "GUACHENÉ"
    },
    "19318": {
        "Municipio": "GUAPI"
    },
    "19355": {
        "Municipio": "INZÁ"
    },
    "19364": {
        "Municipio": "JAMBALÓ"
    },
    "19392": {
        "Municipio": "LA SIERRA"
    },
    "19397": {
        "Municipio": "LA VEGA"
    },
    "19418": {
        "Municipio": "LÓPEZ DE MICAY"
    },
    "19450": {
        "Municipio": "MERCADERES"
    },
    "19455": {
        "Municipio": "MIRANDA"
    },
    "19473": {
        "Municipio": "MORALES"
    },
    "19513": {
        "Municipio": "PADILLA"
    },
    "19517": {
        "Municipio": "PÁEZ"
    },
    "19532": {
        "Municipio": "PATÍA"
    },
    "19533": {
        "Municipio": "PIAMONTE"
    },
    "19548": {
        "Municipio": "PIENDAMÓ - TUNÍA"
    },
    "19573": {
        "Municipio": "PUERTO TEJADA"
    },
    "19585": {
        "Municipio": "PURACÉ"
    },
    "19622": {
        "Municipio": "ROSAS"
    },
    "19693": {
        "Municipio": "SAN SEBASTIÁN"
    },
    "19698": {
        "Municipio": "SANTANDER DE QUILICHAO"
    },
    "19701": {
        "Municipio": "SANTA ROSA"
    },
    "19743": {
        "Municipio": "SILVIA"
    },
    "19760": {
        "Municipio": "SOTARÁ - PAISPAMBA"
    },
    "19780": {
        "Municipio": "SUÁREZ"
    },
    "19785": {
        "Municipio": "SUCRE"
    },
    "19807": {
        "Municipio": "TIMBÍO"
    },
    "19809": {
        "Municipio": "TIMBIQUÍ"
    },
    "19821": {
        "Municipio": "TORIBÍO"
    },
    "19824": {
        "Municipio": "TOTORÓ"
    },
    "19845": {
        "Municipio": "VILLA RICA"
    },
    "20001": {
        "Municipio": "VALLEDUPAR"
    },
    "20011": {
        "Municipio": "AGUACHICA"
    },
    "20013": {
        "Municipio": "AGUSTÍN CODAZZI"
    },
    "20032": {
        "Municipio": "ASTREA"
    },
    "20045": {
        "Municipio": "BECERRIL"
    },
    "20060": {
        "Municipio": "BOSCONIA"
    },
    "20175": {
        "Municipio": "CHIMICHAGUA"
    },
    "20178": {
        "Municipio": "CHIRIGUANÁ"
    },
    "20228": {
        "Municipio": "CURUMANÍ"
    },
    "20238": {
        "Municipio": "EL COPEY"
    },
    "20250": {
        "Municipio": "EL PASO"
    },
    "20295": {
        "Municipio": "GAMARRA"
    },
    "20310": {
        "Municipio": "GONZÁLEZ"
    },
    "20383": {
        "Municipio": "LA GLORIA"
    },
    "20400": {
        "Municipio": "LA JAGUA DE IBIRICO"
    },
    "20443": {
        "Municipio": "MANAURE BALCÓN DEL CESAR"
    },
    "20517": {
        "Municipio": "PAILITAS"
    },
    "20550": {
        "Municipio": "PELAYA"
    },
    "20570": {
        "Municipio": "PUEBLO BELLO"
    },
    "20614": {
        "Municipio": "RÍO DE ORO"
    },
    "20621": {
        "Municipio": "LA PAZ"
    },
    "20710": {
        "Municipio": "SAN ALBERTO"
    },
    "20750": {
        "Municipio": "SAN DIEGO"
    },
    "20770": {
        "Municipio": "SAN MARTÍN"
    },
    "20787": {
        "Municipio": "TAMALAMEQUE"
    },
    "23001": {
        "Municipio": "MONTERÍA"
    },
    "23068": {
        "Municipio": "AYAPEL"
    },
    "23079": {
        "Municipio": "BUENAVISTA"
    },
    "23090": {
        "Municipio": "CANALETE"
    },
    "23162": {
        "Municipio": "CERETÉ"
    },
    "23168": {
        "Municipio": "CHIMÁ"
    },
    "23182": {
        "Municipio": "CHINÚ"
    },
    "23189": {
        "Municipio": "CIÉNAGA DE ORO"
    },
    "23300": {
        "Municipio": "COTORRA"
    },
    "23350": {
        "Municipio": "LA APARTADA"
    },
    "23417": {
        "Municipio": "LORICA"
    },
    "23419": {
        "Municipio": "LOS CÓRDOBAS"
    },
    "23464": {
        "Municipio": "MOMIL"
    },
    "23466": {
        "Municipio": "MONTELÍBANO"
    },
    "23500": {
        "Municipio": "MOÑITOS"
    },
    "23555": {
        "Municipio": "PLANETA RICA"
    },
    "23570": {
        "Municipio": "PUEBLO NUEVO"
    },
    "23574": {
        "Municipio": "PUERTO ESCONDIDO"
    },
    "23580": {
        "Municipio": "PUERTO LIBERTADOR"
    },
    "23586": {
        "Municipio": "PURÍSIMA DE LA CONCEPCIÓN"
    },
    "23660": {
        "Municipio": "SAHAGÚN"
    },
    "23670": {
        "Municipio": "SAN ANDRÉS DE SOTAVENTO"
    },
    "23672": {
        "Municipio": "SAN ANTERO"
    },
    "23675": {
        "Municipio": "SAN BERNARDO DEL VIENTO"
    },
    "23678": {
        "Municipio": "SAN CARLOS"
    },
    "23682": {
        "Municipio": "SAN JOSÉ DE URÉ"
    },
    "23686": {
        "Municipio": "SAN PELAYO"
    },
    "23807": {
        "Municipio": "TIERRALTA"
    },
    "23815": {
        "Municipio": "TUCHÍN"
    },
    "23855": {
        "Municipio": "VALENCIA"
    },
    "25001": {
        "Municipio": "AGUA DE DIOS"
    },
    "25019": {
        "Municipio": "ALBÁN"
    },
    "25035": {
        "Municipio": "ANAPOIMA"
    },
    "25040": {
        "Municipio": "ANOLAIMA"
    },
    "25053": {
        "Municipio": "ARBELÁEZ"
    },
    "25086": {
        "Municipio": "BELTRÁN"
    },
    "25095": {
        "Municipio": "BITUIMA"
    },
    "25099": {
        "Municipio": "BOJACÁ"
    },
    "25120": {
        "Municipio": "CABRERA"
    },
    "25123": {
        "Municipio": "CACHIPAY"
    },
    "25126": {
        "Municipio": "CAJICÁ"
    },
    "25148": {
        "Municipio": "CAPARRAPÍ"
    },
    "25151": {
        "Municipio": "CÁQUEZA"
    },
    "25154": {
        "Municipio": "CARMEN DE CARUPA"
    },
    "25168": {
        "Municipio": "CHAGUANÍ"
    },
    "25175": {
        "Municipio": "CHÍA"
    },
    "25178": {
        "Municipio": "CHIPAQUE"
    },
    "25181": {
        "Municipio": "CHOACHÍ"
    },
    "25183": {
        "Municipio": "CHOCONTÁ"
    },
    "25200": {
        "Municipio": "COGUA"
    },
    "25214": {
        "Municipio": "COTA"
    },
    "25224": {
        "Municipio": "CUCUNUBÁ"
    },
    "25245": {
        "Municipio": "EL COLEGIO"
    },
    "25258": {
        "Municipio": "EL PEÑÓN"
    },
    "25260": {
        "Municipio": "EL ROSAL"
    },
    "25269": {
        "Municipio": "FACATATIVÁ"
    },
    "25279": {
        "Municipio": "FÓMEQUE"
    },
    "25281": {
        "Municipio": "FOSCA"
    },
    "25286": {
        "Municipio": "FUNZA"
    },
    "25288": {
        "Municipio": "FÚQUENE"
    },
    "25290": {
        "Municipio": "FUSAGASUGÁ"
    },
    "25293": {
        "Municipio": "GACHALÁ"
    },
    "25295": {
        "Municipio": "GACHANCIPÁ"
    },
    "25297": {
        "Municipio": "GACHETÁ"
    },
    "25299": {
        "Municipio": "GAMA"
    },
    "25307": {
        "Municipio": "GIRARDOT"
    },
    "25312": {
        "Municipio": "GRANADA"
    },
    "25317": {
        "Municipio": "GUACHETÁ"
    },
    "25320": {
        "Municipio": "GUADUAS"
    },
    "25322": {
        "Municipio": "GUASCA"
    },
    "25324": {
        "Municipio": "GUATAQUÍ"
    },
    "25326": {
        "Municipio": "GUATAVITA"
    },
    "25328": {
        "Municipio": "GUAYABAL DE SÍQUIMA"
    },
    "25335": {
        "Municipio": "GUAYABETAL"
    },
    "25339": {
        "Municipio": "GUTIÉRREZ"
    },
    "25368": {
        "Municipio": "JERUSALÉN"
    },
    "25372": {
        "Municipio": "JUNÍN"
    },
    "25377": {
        "Municipio": "LA CALERA"
    },
    "25386": {
        "Municipio": "LA MESA"
    },
    "25394": {
        "Municipio": "LA PALMA"
    },
    "25398": {
        "Municipio": "LA PEÑA"
    },
    "25402": {
        "Municipio": "LA VEGA"
    },
    "25407": {
        "Municipio": "LENGUAZAQUE"
    },
    "25426": {
        "Municipio": "MACHETÁ"
    },
    "25430": {
        "Municipio": "MADRID"
    },
    "25436": {
        "Municipio": "MANTA"
    },
    "25438": {
        "Municipio": "MEDINA"
    },
    "25473": {
        "Municipio": "MOSQUERA"
    },
    "25483": {
        "Municipio": "NARIÑO"
    },
    "25486": {
        "Municipio": "NEMOCÓN"
    },
    "25488": {
        "Municipio": "NILO"
    },
    "25489": {
        "Municipio": "NIMAIMA"
    },
    "25491": {
        "Municipio": "NOCAIMA"
    },
    "25506": {
        "Municipio": "VENECIA"
    },
    "25513": {
        "Municipio": "PACHO"
    },
    "25518": {
        "Municipio": "PAIME"
    },
    "25524": {
        "Municipio": "PANDI"
    },
    "25530": {
        "Municipio": "PARATEBUENO"
    },
    "25535": {
        "Municipio": "PASCA"
    },
    "25572": {
        "Municipio": "PUERTO SALGAR"
    },
    "25580": {
        "Municipio": "PULÍ"
    },
    "25592": {
        "Municipio": "QUEBRADANEGRA"
    },
    "25594": {
        "Municipio": "QUETAME"
    },
    "25596": {
        "Municipio": "QUIPILE"
    },
    "25599": {
        "Municipio": "APULO"
    },
    "25612": {
        "Municipio": "RICAURTE"
    },
    "25645": {
        "Municipio": "SAN ANTONIO DEL TEQUENDAMA"
    },
    "25649": {
        "Municipio": "SAN BERNARDO"
    },
    "25653": {
        "Municipio": "SAN CAYETANO"
    },
    "25658": {
        "Municipio": "SAN FRANCISCO"
    },
    "25662": {
        "Municipio": "SAN JUAN DE RIOSECO"
    },
    "25718": {
        "Municipio": "SASAIMA"
    },
    "25736": {
        "Municipio": "SESQUILÉ"
    },
    "25740": {
        "Municipio": "SIBATÉ"
    },
    "25743": {
        "Municipio": "SILVANIA"
    },
    "25745": {
        "Municipio": "SIMIJACA"
    },
    "25754": {
        "Municipio": "SOACHA"
    },
    "25758": {
        "Municipio": "SOPÓ"
    },
    "25769": {
        "Municipio": "SUBACHOQUE"
    },
    "25772": {
        "Municipio": "SUESCA"
    },
    "25777": {
        "Municipio": "SUPATÁ"
    },
    "25779": {
        "Municipio": "SUSA"
    },
    "25781": {
        "Municipio": "SUTATAUSA"
    },
    "25785": {
        "Municipio": "TABIO"
    },
    "25793": {
        "Municipio": "TAUSA"
    },
    "25797": {
        "Municipio": "TENA"
    },
    "25799": {
        "Municipio": "TENJO"
    },
    "25805": {
        "Municipio": "TIBACUY"
    },
    "25807": {
        "Municipio": "TIBIRITA"
    },
    "25815": {
        "Municipio": "TOCAIMA"
    },
    "25817": {
        "Municipio": "TOCANCIPÁ"
    },
    "25823": {
        "Municipio": "TOPAIPÍ"
    },
    "25839": {
        "Municipio": "UBALÁ"
    },
    "25841": {
        "Municipio": "UBAQUE"
    },
    "25843": {
        "Municipio": "VILLA DE SAN DIEGO DE UBATÉ"
    },
    "25845": {
        "Municipio": "UNE"
    },
    "25851": {
        "Municipio": "ÚTICA"
    },
    "25862": {
        "Municipio": "VERGARA"
    },
    "25867": {
        "Municipio": "VIANÍ"
    },
    "25871": {
        "Municipio": "VILLAGÓMEZ"
    },
    "25873": {
        "Municipio": "VILLAPINZÓN"
    },
    "25875": {
        "Municipio": "VILLETA"
    },
    "25878": {
        "Municipio": "VIOTÁ"
    },
    "25885": {
        "Municipio": "YACOPÍ"
    },
    "25898": {
        "Municipio": "ZIPACÓN"
    },
    "25899": {
        "Municipio": "ZIPAQUIRÁ"
    },
    "27001": {
        "Municipio": "QUIBDÓ"
    },
    "27006": {
        "Municipio": "ACANDÍ"
    },
    "27025": {
        "Municipio": "ALTO BAUDÓ"
    },
    "27050": {
        "Municipio": "ATRATO"
    },
    "27073": {
        "Municipio": "BAGADÓ"
    },
    "27075": {
        "Municipio": "BAHÍA SOLANO"
    },
    "27077": {
        "Municipio": "BAJO BAUDÓ"
    },
    "27099": {
        "Municipio": "BOJAYÁ"
    },
    "27135": {
        "Municipio": "EL CANTÓN DEL SAN PABLO"
    },
    "27150": {
        "Municipio": "CARMEN DEL DARIÉN"
    },
    "27160": {
        "Municipio": "CÉRTEGUI"
    },
    "27205": {
        "Municipio": "CONDOTO"
    },
    "27245": {
        "Municipio": "EL CARMEN DE ATRATO"
    },
    "27250": {
        "Municipio": "EL LITORAL DEL SAN JUAN"
    },
    "27361": {
        "Municipio": "ISTMINA"
    },
    "27372": {
        "Municipio": "JURADÓ"
    },
    "27413": {
        "Municipio": "LLORÓ"
    },
    "27425": {
        "Municipio": "MEDIO ATRATO"
    },
    "27430": {
        "Municipio": "MEDIO BAUDÓ"
    },
    "27450": {
        "Municipio": "MEDIO SAN JUAN"
    },
    "27491": {
        "Municipio": "NÓVITA"
    },
    "27495": {
        "Municipio": "NUQUÍ"
    },
    "27580": {
        "Municipio": "RÍO IRÓ"
    },
    "27600": {
        "Municipio": "RÍO QUITO"
    },
    "27615": {
        "Municipio": "RIOSUCIO"
    },
    "27660": {
        "Municipio": "SAN JOSÉ DEL PALMAR"
    },
    "27745": {
        "Municipio": "SIPÍ"
    },
    "27787": {
        "Municipio": "TADÓ"
    },
    "27800": {
        "Municipio": "UNGUÍA"
    },
    "27810": {
        "Municipio": "UNIÓN PANAMERICANA"
    },
    "41001": {
        "Municipio": "NEIVA"
    },
    "41006": {
        "Municipio": "ACEVEDO"
    },
    "41013": {
        "Municipio": "AGRADO"
    },
    "41016": {
        "Municipio": "AIPE"
    },
    "41020": {
        "Municipio": "ALGECIRAS"
    },
    "41026": {
        "Municipio": "ALTAMIRA"
    },
    "41078": {
        "Municipio": "BARAYA"
    },
    "41132": {
        "Municipio": "CAMPOALEGRE"
    },
    "41206": {
        "Municipio": "COLOMBIA"
    },
    "41244": {
        "Municipio": "ELÍAS"
    },
    "41298": {
        "Municipio": "GARZÓN"
    },
    "41306": {
        "Municipio": "GIGANTE"
    },
    "41319": {
        "Municipio": "GUADALUPE"
    },
    "41349": {
        "Municipio": "HOBO"
    },
    "41357": {
        "Municipio": "ÍQUIRA"
    },
    "41359": {
        "Municipio": "ISNOS"
    },
    "41378": {
        "Municipio": "LA ARGENTINA"
    },
    "41396": {
        "Municipio": "LA PLATA"
    },
    "41483": {
        "Municipio": "NÁTAGA"
    },
    "41503": {
        "Municipio": "OPORAPA"
    },
    "41518": {
        "Municipio": "PAICOL"
    },
    "41524": {
        "Municipio": "PALERMO"
    },
    "41530": {
        "Municipio": "PALESTINA"
    },
    "41548": {
        "Municipio": "PITAL"
    },
    "41551": {
        "Municipio": "PITALITO"
    },
    "41615": {
        "Municipio": "RIVERA"
    },
    "41660": {
        "Municipio": "SALADOBLANCO"
    },
    "41668": {
        "Municipio": "SAN AGUSTÍN"
    },
    "41676": {
        "Municipio": "SANTA MARÍA"
    },
    "41770": {
        "Municipio": "SUAZA"
    },
    "41791": {
        "Municipio": "TARQUI"
    },
    "41797": {
        "Municipio": "TESALIA"
    },
    "41799": {
        "Municipio": "TELLO"
    },
    "41801": {
        "Municipio": "TERUEL"
    },
    "41807": {
        "Municipio": "TIMANÁ"
    },
    "41872": {
        "Municipio": "VILLAVIEJA"
    },
    "41885": {
        "Municipio": "YAGUARÁ"
    },
    "44001": {
        "Municipio": "RIOHACHA"
    },
    "44035": {
        "Municipio": "ALBANIA"
    },
    "44078": {
        "Municipio": "BARRANCAS"
    },
    "44090": {
        "Municipio": "DIBULLA"
    },
    "44098": {
        "Municipio": "DISTRACCIÓN"
    },
    "44110": {
        "Municipio": "EL MOLINO"
    },
    "44279": {
        "Municipio": "FONSECA"
    },
    "44378": {
        "Municipio": "HATONUEVO"
    },
    "44420": {
        "Municipio": "LA JAGUA DEL PILAR"
    },
    "44430": {
        "Municipio": "MAICAO"
    },
    "44560": {
        "Municipio": "MANAURE"
    },
    "44650": {
        "Municipio": "SAN JUAN DEL CESAR"
    },
    "44847": {
        "Municipio": "URIBIA"
    },
    "44855": {
        "Municipio": "URUMITA"
    },
    "44874": {
        "Municipio": "VILLANUEVA"
    },
    "47001": {
        "Municipio": "SANTA MARTA"
    },
    "47030": {
        "Municipio": "ALGARROBO"
    },
    "47053": {
        "Municipio": "ARACATACA"
    },
    "47058": {
        "Municipio": "ARIGUANÍ"
    },
    "47161": {
        "Municipio": "CERRO DE SAN ANTONIO"
    },
    "47170": {
        "Municipio": "CHIVOLO"
    },
    "47189": {
        "Municipio": "CIÉNAGA"
    },
    "47205": {
        "Municipio": "CONCORDIA"
    },
    "47245": {
        "Municipio": "EL BANCO"
    },
    "47258": {
        "Municipio": "EL PIÑÓN"
    },
    "47268": {
        "Municipio": "EL RETÉN"
    },
    "47288": {
        "Municipio": "FUNDACIÓN"
    },
    "47318": {
        "Municipio": "GUAMAL"
    },
    "47460": {
        "Municipio": "NUEVA GRANADA"
    },
    "47541": {
        "Municipio": "PEDRAZA"
    },
    "47545": {
        "Municipio": "PIJIÑO DEL CARMEN"
    },
    "47551": {
        "Municipio": "PIVIJAY"
    },
    "47555": {
        "Municipio": "PLATO"
    },
    "47570": {
        "Municipio": "PUEBLOVIEJO"
    },
    "47605": {
        "Municipio": "REMOLINO"
    },
    "47660": {
        "Municipio": "SABANAS DE SAN ÁNGEL"
    },
    "47675": {
        "Municipio": "SALAMINA"
    },
    "47692": {
        "Municipio": "SAN SEBASTIÁN DE BUENAVISTA"
    },
    "47703": {
        "Municipio": "SAN ZENÓN"
    },
    "47707": {
        "Municipio": "SANTA ANA"
    },
    "47720": {
        "Municipio": "SANTA BÁRBARA DE PINTO"
    },
    "47745": {
        "Municipio": "SITIONUEVO"
    },
    "47798": {
        "Municipio": "TENERIFE"
    },
    "47960": {
        "Municipio": "ZAPAYÁN"
    },
    "47980": {
        "Municipio": "ZONA BANANERA"
    },
    "50001": {
        "Municipio": "VILLAVICENCIO"
    },
    "50006": {
        "Municipio": "ACACÍAS"
    },
    "50110": {
        "Municipio": "BARRANCA DE UPÍA"
    },
    "50124": {
        "Municipio": "CABUYARO"
    },
    "50150": {
        "Municipio": "CASTILLA LA NUEVA"
    },
    "50223": {
        "Municipio": "CUBARRAL"
    },
    "50226": {
        "Municipio": "CUMARAL"
    },
    "50245": {
        "Municipio": "EL CALVARIO"
    },
    "50251": {
        "Municipio": "EL CASTILLO"
    },
    "50270": {
        "Municipio": "EL DORADO"
    },
    "50287": {
        "Municipio": "FUENTE DE ORO"
    },
    "50313": {
        "Municipio": "GRANADA"
    },
    "50318": {
        "Municipio": "GUAMAL"
    },
    "50325": {
        "Municipio": "MAPIRIPÁN"
    },
    "50330": {
        "Municipio": "MESETAS"
    },
    "50350": {
        "Municipio": "LA MACARENA"
    },
    "50370": {
        "Municipio": "URIBE"
    },
    "50400": {
        "Municipio": "LEJANÍAS"
    },
    "50450": {
        "Municipio": "PUERTO CONCORDIA"
    },
    "50568": {
        "Municipio": "PUERTO GAITÁN"
    },
    "50573": {
        "Municipio": "PUERTO LÓPEZ"
    },
    "50577": {
        "Municipio": "PUERTO LLERAS"
    },
    "50590": {
        "Municipio": "PUERTO RICO"
    },
    "50606": {
        "Municipio": "RESTREPO"
    },
    "50680": {
        "Municipio": "SAN CARLOS DE GUAROA"
    },
    "50683": {
        "Municipio": "SAN JUAN DE ARAMA"
    },
    "50686": {
        "Municipio": "SAN JUANITO"
    },
    "50689": {
        "Municipio": "SAN MARTÍN"
    },
    "50711": {
        "Municipio": "VISTAHERMOSA"
    },
    "52001": {
        "Municipio": "PASTO"
    },
    "52019": {
        "Municipio": "ALBÁN"
    },
    "52022": {
        "Municipio": "ALDANA"
    },
    "52036": {
        "Municipio": "ANCUYA"
    },
    "52051": {
        "Municipio": "ARBOLEDA"
    },
    "52079": {
        "Municipio": "BARBACOAS"
    },
    "52083": {
        "Municipio": "BELÉN"
    },
    "52110": {
        "Municipio": "BUESACO"
    },
    "52203": {
        "Municipio": "COLÓN"
    },
    "52207": {
        "Municipio": "CONSACÁ"
    },
    "52210": {
        "Municipio": "CONTADERO"
    },
    "52215": {
        "Municipio": "CÓRDOBA"
    },
    "52224": {
        "Municipio": "CUASPUD CARLOSAMA"
    },
    "52227": {
        "Municipio": "CUMBAL"
    },
    "52233": {
        "Municipio": "CUMBITARA"
    },
    "52240": {
        "Municipio": "CHACHAGÜÍ"
    },
    "52250": {
        "Municipio": "EL CHARCO"
    },
    "52254": {
        "Municipio": "EL PEÑOL"
    },
    "52256": {
        "Municipio": "EL ROSARIO"
    },
    "52258": {
        "Municipio": "EL TABLÓN DE GÓMEZ"
    },
    "52260": {
        "Municipio": "EL TAMBO"
    },
    "52287": {
        "Municipio": "FUNES"
    },
    "52317": {
        "Municipio": "GUACHUCAL"
    },
    "52320": {
        "Municipio": "GUAITARILLA"
    },
    "52323": {
        "Municipio": "GUALMATÁN"
    },
    "52352": {
        "Municipio": "ILES"
    },
    "52354": {
        "Municipio": "IMUÉS"
    },
    "52356": {
        "Municipio": "IPIALES"
    },
    "52378": {
        "Municipio": "LA CRUZ"
    },
    "52381": {
        "Municipio": "LA FLORIDA"
    },
    "52385": {
        "Municipio": "LA LLANADA"
    },
    "52390": {
        "Municipio": "LA TOLA"
    },
    "52399": {
        "Municipio": "LA UNIÓN"
    },
    "52405": {
        "Municipio": "LEIVA"
    },
    "52411": {
        "Municipio": "LINARES"
    },
    "52418": {
        "Municipio": "LOS ANDES"
    },
    "52427": {
        "Municipio": "MAGÜÍ"
    },
    "52435": {
        "Municipio": "MALLAMA"
    },
    "52473": {
        "Municipio": "MOSQUERA"
    },
    "52480": {
        "Municipio": "NARIÑO"
    },
    "52490": {
        "Municipio": "OLAYA HERRERA"
    },
    "52506": {
        "Municipio": "OSPINA"
    },
    "52520": {
        "Municipio": "FRANCISCO PIZARRO"
    },
    "52540": {
        "Municipio": "POLICARPA"
    },
    "52560": {
        "Municipio": "POTOSÍ"
    },
    "52565": {
        "Municipio": "PROVIDENCIA"
    },
    "52573": {
        "Municipio": "PUERRES"
    },
    "52585": {
        "Municipio": "PUPIALES"
    },
    "52612": {
        "Municipio": "RICAURTE"
    },
    "52621": {
        "Municipio": "ROBERTO PAYÁN"
    },
    "52678": {
        "Municipio": "SAMANIEGO"
    },
    "52683": {
        "Municipio": "SANDONÁ"
    },
    "52685": {
        "Municipio": "SAN BERNARDO"
    },
    "52687": {
        "Municipio": "SAN LORENZO"
    },
    "52693": {
        "Municipio": "SAN PABLO"
    },
    "52694": {
        "Municipio": "SAN PEDRO DE CARTAGO"
    },
    "52696": {
        "Municipio": "SANTA BÁRBARA"
    },
    "52699": {
        "Municipio": "SANTACRUZ"
    },
    "52720": {
        "Municipio": "SAPUYES"
    },
    "52786": {
        "Municipio": "TAMINANGO"
    },
    "52788": {
        "Municipio": "TANGUA"
    },
    "52835": {
        "Municipio": "SAN ANDRÉS DE TUMACO"
    },
    "52838": {
        "Municipio": "TÚQUERRES"
    },
    "52885": {
        "Municipio": "YACUANQUER"
    },
    "54001": {
        "Municipio": "SAN JOSÉ DE CÚCUTA"
    },
    "54003": {
        "Municipio": "ÁBREGO"
    },
    "54051": {
        "Municipio": "ARBOLEDAS"
    },
    "54099": {
        "Municipio": "BOCHALEMA"
    },
    "54109": {
        "Municipio": "BUCARASICA"
    },
    "54125": {
        "Municipio": "CÁCOTA"
    },
    "54128": {
        "Municipio": "CÁCHIRA"
    },
    "54172": {
        "Municipio": "CHINÁCOTA"
    },
    "54174": {
        "Municipio": "CHITAGÁ"
    },
    "54206": {
        "Municipio": "CONVENCIÓN"
    },
    "54223": {
        "Municipio": "CUCUTILLA"
    },
    "54239": {
        "Municipio": "DURANIA"
    },
    "54245": {
        "Municipio": "EL CARMEN"
    },
    "54250": {
        "Municipio": "EL TARRA"
    },
    "54261": {
        "Municipio": "EL ZULIA"
    },
    "54313": {
        "Municipio": "GRAMALOTE"
    },
    "54344": {
        "Municipio": "HACARÍ"
    },
    "54347": {
        "Municipio": "HERRÁN"
    },
    "54377": {
        "Municipio": "LABATECA"
    },
    "54385": {
        "Municipio": "LA ESPERANZA"
    },
    "54398": {
        "Municipio": "LA PLAYA"
    },
    "54405": {
        "Municipio": "LOS PATIOS"
    },
    "54418": {
        "Municipio": "LOURDES"
    },
    "54480": {
        "Municipio": "MUTISCUA"
    },
    "54498": {
        "Municipio": "OCAÑA"
    },
    "54518": {
        "Municipio": "PAMPLONA"
    },
    "54520": {
        "Municipio": "PAMPLONITA"
    },
    "54553": {
        "Municipio": "PUERTO SANTANDER"
    },
    "54599": {
        "Municipio": "RAGONVALIA"
    },
    "54660": {
        "Municipio": "SALAZAR"
    },
    "54670": {
        "Municipio": "SAN CALIXTO"
    },
    "54673": {
        "Municipio": "SAN CAYETANO"
    },
    "54680": {
        "Municipio": "SANTIAGO"
    },
    "54720": {
        "Municipio": "SARDINATA"
    },
    "54743": {
        "Municipio": "SILOS"
    },
    "54800": {
        "Municipio": "TEORAMA"
    },
    "54810": {
        "Municipio": "TIBÚ"
    },
    "54820": {
        "Municipio": "TOLEDO"
    },
    "54871": {
        "Municipio": "VILLA CARO"
    },
    "54874": {
        "Municipio": "VILLA DEL ROSARIO"
    },
    "63001": {
        "Municipio": "ARMENIA"
    },
    "63111": {
        "Municipio": "BUENAVISTA"
    },
    "63130": {
        "Municipio": "CALARCÁ"
    },
    "63190": {
        "Municipio": "CIRCASIA"
    },
    "63212": {
        "Municipio": "CÓRDOBA"
    },
    "63272": {
        "Municipio": "FILANDIA"
    },
    "63302": {
        "Municipio": "GÉNOVA"
    },
    "63401": {
        "Municipio": "LA TEBAIDA"
    },
    "63470": {
        "Municipio": "MONTENEGRO"
    },
    "63548": {
        "Municipio": "PIJAO"
    },
    "63594": {
        "Municipio": "QUIMBAYA"
    },
    "63690": {
        "Municipio": "SALENTO"
    },
    "66001": {
        "Municipio": "PEREIRA"
    },
    "66045": {
        "Municipio": "APÍA"
    },
    "66075": {
        "Municipio": "BALBOA"
    },
    "66088": {
        "Municipio": "BELÉN DE UMBRÍA"
    },
    "66170": {
        "Municipio": "DOSQUEBRADAS"
    },
    "66318": {
        "Municipio": "GUÁTICA"
    },
    "66383": {
        "Municipio": "LA CELIA"
    },
    "66400": {
        "Municipio": "LA VIRGINIA"
    },
    "66440": {
        "Municipio": "MARSELLA"
    },
    "66456": {
        "Municipio": "MISTRATÓ"
    },
    "66572": {
        "Municipio": "PUEBLO RICO"
    },
    "66594": {
        "Municipio": "QUINCHÍA"
    },
    "66682": {
        "Municipio": "SANTA ROSA DE CABAL"
    },
    "66687": {
        "Municipio": "SANTUARIO"
    },
    "68001": {
        "Municipio": "BUCARAMANGA"
    },
    "68013": {
        "Municipio": "AGUADA"
    },
    "68020": {
        "Municipio": "ALBANIA"
    },
    "68051": {
        "Municipio": "ARATOCA"
    },
    "68077": {
        "Municipio": "BARBOSA"
    },
    "68079": {
        "Municipio": "BARICHARA"
    },
    "68081": {
        "Municipio": "BARRANCABERMEJA"
    },
    "68092": {
        "Municipio": "BETULIA"
    },
    "68101": {
        "Municipio": "BOLÍVAR"
    },
    "68121": {
        "Municipio": "CABRERA"
    },
    "68132": {
        "Municipio": "CALIFORNIA"
    },
    "68147": {
        "Municipio": "CAPITANEJO"
    },
    "68152": {
        "Municipio": "CARCASÍ"
    },
    "68160": {
        "Municipio": "CEPITÁ"
    },
    "68162": {
        "Municipio": "CERRITO"
    },
    "68167": {
        "Municipio": "CHARALÁ"
    },
    "68169": {
        "Municipio": "CHARTA"
    },
    "68176": {
        "Municipio": "CHIMA"
    },
    "68179": {
        "Municipio": "CHIPATÁ"
    },
    "68190": {
        "Municipio": "CIMITARRA"
    },
    "68207": {
        "Municipio": "CONCEPCIÓN"
    },
    "68209": {
        "Municipio": "CONFINES"
    },
    "68211": {
        "Municipio": "CONTRATACIÓN"
    },
    "68217": {
        "Municipio": "COROMORO"
    },
    "68229": {
        "Municipio": "CURITÍ"
    },
    "68235": {
        "Municipio": "EL CARMEN DE CHUCURÍ"
    },
    "68245": {
        "Municipio": "EL GUACAMAYO"
    },
    "68250": {
        "Municipio": "EL PEÑÓN"
    },
    "68255": {
        "Municipio": "EL PLAYÓN"
    },
    "68264": {
        "Municipio": "ENCINO"
    },
    "68266": {
        "Municipio": "ENCISO"
    },
    "68271": {
        "Municipio": "FLORIÁN"
    },
    "68276": {
        "Municipio": "FLORIDABLANCA"
    },
    "68296": {
        "Municipio": "GALÁN"
    },
    "68298": {
        "Municipio": "GÁMBITA"
    },
    "68307": {
        "Municipio": "GIRÓN"
    },
    "68318": {
        "Municipio": "GUACA"
    },
    "68320": {
        "Municipio": "GUADALUPE"
    },
    "68322": {
        "Municipio": "GUAPOTÁ"
    },
    "68324": {
        "Municipio": "GUAVATÁ"
    },
    "68327": {
        "Municipio": "GÜEPSA"
    },
    "68344": {
        "Municipio": "HATO"
    },
    "68368": {
        "Municipio": "JESÚS MARÍA"
    },
    "68370": {
        "Municipio": "JORDÁN"
    },
    "68377": {
        "Municipio": "LA BELLEZA"
    },
    "68385": {
        "Municipio": "LANDÁZURI"
    },
    "68397": {
        "Municipio": "LA PAZ"
    },
    "68406": {
        "Municipio": "LEBRIJA"
    },
    "68418": {
        "Municipio": "LOS SANTOS"
    },
    "68425": {
        "Municipio": "MACARAVITA"
    },
    "68432": {
        "Municipio": "MÁLAGA"
    },
    "68444": {
        "Municipio": "MATANZA"
    },
    "68464": {
        "Municipio": "MOGOTES"
    },
    "68468": {
        "Municipio": "MOLAGAVITA"
    },
    "68498": {
        "Municipio": "OCAMONTE"
    },
    "68500": {
        "Municipio": "OIBA"
    },
    "68502": {
        "Municipio": "ONZAGA"
    },
    "68522": {
        "Municipio": "PALMAR"
    },
    "68524": {
        "Municipio": "PALMAS DEL SOCORRO"
    },
    "68533": {
        "Municipio": "PÁRAMO"
    },
    "68547": {
        "Municipio": "PIEDECUESTA"
    },
    "68549": {
        "Municipio": "PINCHOTE"
    },
    "68572": {
        "Municipio": "PUENTE NACIONAL"
    },
    "68573": {
        "Municipio": "PUERTO PARRA"
    },
    "68575": {
        "Municipio": "PUERTO WILCHES"
    },
    "68615": {
        "Municipio": "RIONEGRO"
    },
    "68655": {
        "Municipio": "SABANA DE TORRES"
    },
    "68669": {
        "Municipio": "SAN ANDRÉS"
    },
    "68673": {
        "Municipio": "SAN BENITO"
    },
    "68679": {
        "Municipio": "SAN GIL"
    },
    "68682": {
        "Municipio": "SAN JOAQUÍN"
    },
    "68684": {
        "Municipio": "SAN JOSÉ DE MIRANDA"
    },
    "68686": {
        "Municipio": "SAN MIGUEL"
    },
    "68689": {
        "Municipio": "SAN VICENTE DE CHUCURÍ"
    },
    "68705": {
        "Municipio": "SANTA BÁRBARA"
    },
    "68720": {
        "Municipio": "SANTA HELENA DEL OPÓN"
    },
    "68745": {
        "Municipio": "SIMACOTA"
    },
    "68755": {
        "Municipio": "SOCORRO"
    },
    "68770": {
        "Municipio": "SUAITA"
    },
    "68773": {
        "Municipio": "SUCRE"
    },
    "68780": {
        "Municipio": "SURATÁ"
    },
    "68820": {
        "Municipio": "TONA"
    },
    "68855": {
        "Municipio": "VALLE DE SAN JOSÉ"
    },
    "68861": {
        "Municipio": "VÉLEZ"
    },
    "68867": {
        "Municipio": "VETAS"
    },
    "68872": {
        "Municipio": "VILLANUEVA"
    },
    "68895": {
        "Municipio": "ZAPATOCA"
    },
    "70001": {
        "Municipio": "SINCELEJO"
    },
    "70110": {
        "Municipio": "BUENAVISTA"
    },
    "70124": {
        "Municipio": "CAIMITO"
    },
    "70204": {
        "Municipio": "COLOSÓ"
    },
    "70215": {
        "Municipio": "COROZAL"
    },
    "70221": {
        "Municipio": "COVEÑAS"
    },
    "70230": {
        "Municipio": "CHALÁN"
    },
    "70233": {
        "Municipio": "EL ROBLE"
    },
    "70235": {
        "Municipio": "GALERAS"
    },
    "70265": {
        "Municipio": "GUARANDA"
    },
    "70400": {
        "Municipio": "LA UNIÓN"
    },
    "70418": {
        "Municipio": "LOS PALMITOS"
    },
    "70429": {
        "Municipio": "MAJAGUAL"
    },
    "70473": {
        "Municipio": "MORROA"
    },
    "70508": {
        "Municipio": "OVEJAS"
    },
    "70523": {
        "Municipio": "PALMITO"
    },
    "70670": {
        "Municipio": "SAMPUÉS"
    },
    "70678": {
        "Municipio": "SAN BENITO ABAD"
    },
    "70702": {
        "Municipio": "SAN JUAN DE BETULIA"
    },
    "70708": {
        "Municipio": "SAN MARCOS"
    },
    "70713": {
        "Municipio": "SAN ONOFRE"
    },
    "70717": {
        "Municipio": "SAN PEDRO"
    },
    "70742": {
        "Municipio": "SAN LUIS DE SINCÉ"
    },
    "70771": {
        "Municipio": "SUCRE"
    },
    "70820": {
        "Municipio": "SANTIAGO DE TOLÚ"
    },
    "70823": {
        "Municipio": "SAN JOSÉ DE TOLUVIEJO"
    },
    "73001": {
        "Municipio": "IBAGUÉ"
    },
    "73024": {
        "Municipio": "ALPUJARRA"
    },
    "73026": {
        "Municipio": "ALVARADO"
    },
    "73030": {
        "Municipio": "AMBALEMA"
    },
    "73043": {
        "Municipio": "ANZOÁTEGUI"
    },
    "73055": {
        "Municipio": "ARMERO"
    },
    "73067": {
        "Municipio": "ATACO"
    },
    "73124": {
        "Municipio": "CAJAMARCA"
    },
    "73148": {
        "Municipio": "CARMEN DE APICALÁ"
    },
    "73152": {
        "Municipio": "CASABIANCA"
    },
    "73168": {
        "Municipio": "CHAPARRAL"
    },
    "73200": {
        "Municipio": "COELLO"
    },
    "73217": {
        "Municipio": "COYAIMA"
    },
    "73226": {
        "Municipio": "CUNDAY"
    },
    "73236": {
        "Municipio": "DOLORES"
    },
    "73268": {
        "Municipio": "ESPINAL"
    },
    "73270": {
        "Municipio": "FALAN"
    },
    "73275": {
        "Municipio": "FLANDES"
    },
    "73283": {
        "Municipio": "FRESNO"
    },
    "73319": {
        "Municipio": "GUAMO"
    },
    "73347": {
        "Municipio": "HERVEO"
    },
    "73349": {
        "Municipio": "HONDA"
    },
    "73352": {
        "Municipio": "ICONONZO"
    },
    "73408": {
        "Municipio": "LÉRIDA"
    },
    "73411": {
        "Municipio": "LÍBANO"
    },
    "73443": {
        "Municipio": "SAN SEBASTIÁN DE MARIQUITA"
    },
    "73449": {
        "Municipio": "MELGAR"
    },
    "73461": {
        "Municipio": "MURILLO"
    },
    "73483": {
        "Municipio": "NATAGAIMA"
    },
    "73504": {
        "Municipio": "ORTEGA"
    },
    "73520": {
        "Municipio": "PALOCABILDO"
    },
    "73547": {
        "Municipio": "PIEDRAS"
    },
    "73555": {
        "Municipio": "PLANADAS"
    },
    "73563": {
        "Municipio": "PRADO"
    },
    "73585": {
        "Municipio": "PURIFICACIÓN"
    },
    "73616": {
        "Municipio": "RIOBLANCO"
    },
    "73622": {
        "Municipio": "RONCESVALLES"
    },
    "73624": {
        "Municipio": "ROVIRA"
    },
    "73671": {
        "Municipio": "SALDAÑA"
    },
    "73675": {
        "Municipio": "SAN ANTONIO"
    },
    "73678": {
        "Municipio": "SAN LUIS"
    },
    "73686": {
        "Municipio": "SANTA ISABEL"
    },
    "73770": {
        "Municipio": "SUÁREZ"
    },
    "73854": {
        "Municipio": "VALLE DE SAN JUAN"
    },
    "73861": {
        "Municipio": "VENADILLO"
    },
    "73870": {
        "Municipio": "VILLAHERMOSA"
    },
    "73873": {
        "Municipio": "VILLARRICA"
    },
    "76001": {
        "Municipio": "CALI"
    },
    "76020": {
        "Municipio": "ALCALÁ"
    },
    "76036": {
        "Municipio": "ANDALUCÍA"
    },
    "76041": {
        "Municipio": "ANSERMANUEVO"
    },
    "76054": {
        "Municipio": "ARGELIA"
    },
    "76100": {
        "Municipio": "BOLÍVAR"
    },
    "76109": {
        "Municipio": "BUENAVENTURA"
    },
    "76111": {
        "Municipio": "GUADALAJARA DE BUGA"
    },
    "76113": {
        "Municipio": "BUGALAGRANDE"
    },
    "76122": {
        "Municipio": "CAICEDONIA"
    },
    "76126": {
        "Municipio": "CALIMA"
    },
    "76130": {
        "Municipio": "CANDELARIA"
    },
    "76147": {
        "Municipio": "CARTAGO"
    },
    "76233": {
        "Municipio": "DAGUA"
    },
    "76243": {
        "Municipio": "EL ÁGUILA"
    },
    "76246": {
        "Municipio": "EL CAIRO"
    },
    "76248": {
        "Municipio": "EL CERRITO"
    },
    "76250": {
        "Municipio": "EL DOVIO"
    },
    "76275": {
        "Municipio": "FLORIDA"
    },
    "76306": {
        "Municipio": "GINEBRA"
    },
    "76318": {
        "Municipio": "GUACARÍ"
    },
    "76364": {
        "Municipio": "JAMUNDÍ"
    },
    "76377": {
        "Municipio": "LA CUMBRE"
    },
    "76400": {
        "Municipio": "LA UNIÓN"
    },
    "76403": {
        "Municipio": "LA VICTORIA"
    },
    "76497": {
        "Municipio": "OBANDO"
    },
    "76520": {
        "Municipio": "PALMIRA"
    },
    "76563": {
        "Municipio": "PRADERA"
    },
    "76606": {
        "Municipio": "RESTREPO"
    },
    "76616": {
        "Municipio": "RIOFRÍO"
    },
    "76622": {
        "Municipio": "ROLDANILLO"
    },
    "76670": {
        "Municipio": "SAN PEDRO"
    },
    "76736": {
        "Municipio": "SEVILLA"
    },
    "76823": {
        "Municipio": "TORO"
    },
    "76828": {
        "Municipio": "TRUJILLO"
    },
    "76834": {
        "Municipio": "TULUÁ"
    },
    "76845": {
        "Municipio": "ULLOA"
    },
    "76863": {
        "Municipio": "VERSALLES"
    },
    "76869": {
        "Municipio": "VIJES"
    },
    "76890": {
        "Municipio": "YOTOCO"
    },
    "76892": {
        "Municipio": "YUMBO"
    },
    "76895": {
        "Municipio": "ZARZAL"
    },
    "81001": {
        "Municipio": "ARAUCA"
    },
    "81065": {
        "Municipio": "ARAUQUITA"
    },
    "81220": {
        "Municipio": "CRAVO NORTE"
    },
    "81300": {
        "Municipio": "FORTUL"
    },
    "81591": {
        "Municipio": "PUERTO RONDÓN"
    },
    "81736": {
        "Municipio": "SARAVENA"
    },
    "81794": {
        "Municipio": "TAME"
    },
    "85001": {
        "Municipio": "YOPAL"
    },
    "85010": {
        "Municipio": "AGUAZUL"
    },
    "85015": {
        "Municipio": "CHÁMEZA"
    },
    "85125": {
        "Municipio": "HATO COROZAL"
    },
    "85136": {
        "Municipio": "LA SALINA"
    },
    "85139": {
        "Municipio": "MANÍ"
    },
    "85162": {
        "Municipio": "MONTERREY"
    },
    "85225": {
        "Municipio": "NUNCHÍA"
    },
    "85230": {
        "Municipio": "OROCUÉ"
    },
    "85250": {
        "Municipio": "PAZ DE ARIPORO"
    },
    "85263": {
        "Municipio": "PORE"
    },
    "85279": {
        "Municipio": "RECETOR"
    },
    "85300": {
        "Municipio": "SABANALARGA"
    },
    "85315": {
        "Municipio": "SÁCAMA"
    },
    "85325": {
        "Municipio": "SAN LUIS DE PALENQUE"
    },
    "85400": {
        "Municipio": "TÁMARA"
    },
    "85410": {
        "Municipio": "TAURAMENA"
    },
    "85430": {
        "Municipio": "TRINIDAD"
    },
    "85440": {
        "Municipio": "VILLANUEVA"
    },
    "86001": {
        "Municipio": "MOCOA"
    },
    "86219": {
        "Municipio": "COLÓN"
    },
    "86320": {
        "Municipio": "ORITO"
    },
    "86568": {
        "Municipio": "PUERTO ASÍS"
    },
    "86569": {
        "Municipio": "PUERTO CAICEDO"
    },
    "86571": {
        "Municipio": "PUERTO GUZMÁN"
    },
    "86573": {
        "Municipio": "PUERTO LEGUÍZAMO"
    },
    "86749": {
        "Municipio": "SIBUNDOY"
    },
    "86755": {
        "Municipio": "SAN FRANCISCO"
    },
    "86757": {
        "Municipio": "SAN MIGUEL"
    },
    "86760": {
        "Municipio": "SANTIAGO"
    },
    "86865": {
        "Municipio": "VALLE DEL GUAMUEZ"
    },
    "86885": {
        "Municipio": "VILLAGARZÓN"
    },
    "88001": {
        "Municipio": "SAN ANDRÉS"
    },
    "88564": {
        "Municipio": "PROVIDENCIA"
    },
    "91001": {
        "Municipio": "LETICIA"
    },
    "91263": {
        "Municipio": "EL ENCANTO"
    },
    "91405": {
        "Municipio": "LA CHORRERA"
    },
    "91407": {
        "Municipio": "LA PEDRERA"
    },
    "91430": {
        "Municipio": "LA VICTORIA"
    },
    "91460": {
        "Municipio": "MIRITÍ - PARANÁ"
    },
    "91530": {
        "Municipio": "PUERTO ALEGRÍA"
    },
    "91536": {
        "Municipio": "PUERTO ARICA"
    },
    "91540": {
        "Municipio": "PUERTO NARIÑO"
    },
    "91669": {
        "Municipio": "SANTANDER"
    },
    "91798": {
        "Municipio": "TARAPACÁ"
    },
    "94001": {
        "Municipio": "INÍRIDA"
    },
    "94343": {
        "Municipio": "BARRANCOMINAS"
    },
    "94883": {
        "Municipio": "SAN FELIPE"
    },
    "94884": {
        "Municipio": "PUERTO COLOMBIA"
    },
    "94885": {
        "Municipio": "LA GUADALUPE"
    },
    "94886": {
        "Municipio": "CACAHUAL"
    },
    "94887": {
        "Municipio": "PANA-PANA"
    },
    "94888": {
        "Municipio": "MORICHAL"
    },
    "95001": {
        "Municipio": "SAN JOSÉ DEL GUAVIARE"
    },
    "95015": {
        "Municipio": "CALAMAR"
    },
    "95025": {
        "Municipio": "EL RETORNO"
    },
    "95200": {
        "Municipio": "MIRAFLORES"
    },
    "97001": {
        "Municipio": "MITÚ"
    },
    "97161": {
        "Municipio": "CURURÚ"
    },
    "97511": {
        "Municipio": "PACOA"
    },
    "97666": {
        "Municipio": "TARAIRA"
    },
    "97777": {
        "Municipio": "PAPUNAHUA"
    },
    "97889": {
        "Municipio": "YAVARATÉ"
    },
    "99001": {
        "Municipio": "PUERTO CARREÑO"
    },
    "99524": {
        "Municipio": "LA PRIMAVERA"
    },
    "99624": {
        "Municipio": "SANTA ROSALÍA"
    },
    "99773": {
        "Municipio": "CUMARIBO"
    },
    "05001000": {
        "Centro Poblado": "MEDELLÍN, DISTRITO ESPECIAL DE CIENCIA, TECNOLOGÍA E INNOVACIÓN"
    },
    "05001001": {
        "Centro Poblado": "PALMITAS"
    },
    "05001004": {
        "Centro Poblado": "SANTA ELENA"
    },
    "05001009": {
        "Centro Poblado": "ALTAVISTA"
    },
    "05001010": {
        "Centro Poblado": "AGUAS FRÍAS"
    },
    "05001013": {
        "Centro Poblado": "SAN JOSÉ DEL MANZANILLO"
    },
    "05001014": {
        "Centro Poblado": "BARRO BLANCO"
    },
    "05001015": {
        "Centro Poblado": "EL CERRO"
    },
    "05001017": {
        "Centro Poblado": "EL PATIO"
    },
    "05001018": {
        "Centro Poblado": "EL PLACER"
    },
    "05001019": {
        "Centro Poblado": "EL PLAN"
    },
    "05001022": {
        "Centro Poblado": "LA ALDEA"
    },
    "05001023": {
        "Centro Poblado": "LA CUCHILLA"
    },
    "05001025": {
        "Centro Poblado": "LA PALMA"
    },
    "05001027": {
        "Centro Poblado": "LAS PLAYAS"
    },
    "05001029": {
        "Centro Poblado": "PIEDRA GORDA"
    },
    "05001031": {
        "Centro Poblado": "POTRERITO"
    },
    "05001032": {
        "Centro Poblado": "TRAVESÍAS"
    },
    "05001033": {
        "Centro Poblado": "URQUITA"
    },
    "05001035": {
        "Centro Poblado": "BOQUERÓN"
    },
    "05001039": {
        "Centro Poblado": "EL LLANO 1"
    },
    "05001040": {
        "Centro Poblado": "EL LLANO"
    },
    "05001048": {
        "Centro Poblado": "LA VERDE"
    },
    "05001052": {
        "Centro Poblado": "MATASANO"
    },
    "05001054": {
        "Centro Poblado": "MATASANO 2"
    },
    "05001055": {
        "Centro Poblado": "MAZO"
    },
    "05001057": {
        "Centro Poblado": "MEDIA LUNA"
    },
    "05001066": {
        "Centro Poblado": "LAS CAMELIAS"
    },
    "05002000": {
        "Centro Poblado": "ABEJORRAL"
    },
    "05002002": {
        "Centro Poblado": "PANTANILLO"
    },
    "05002004": {
        "Centro Poblado": "NARANJAL - LAS FONDAS"
    },
    "05002016": {
        "Centro Poblado": "LAS CANOAS"
    },
    "05004000": {
        "Centro Poblado": "ABRIAQUÍ"
    },
    "05004003": {
        "Centro Poblado": "POTREROS SECTOR 1"
    },
    "05021000": {
        "Centro Poblado": "ALEJANDRÍA"
    },
    "05030000": {
        "Centro Poblado": "AMAGÁ"
    },
    "05030001": {
        "Centro Poblado": "CAMILO C"
    },
    "05030003": {
        "Centro Poblado": "LA CLARITA"
    },
    "05030004": {
        "Centro Poblado": "LA FERREIRA"
    },
    "05030005": {
        "Centro Poblado": "LA GUALÍ"
    },
    "05030006": {
        "Centro Poblado": "PIEDECUESTA"
    },
    "05030011": {
        "Centro Poblado": "MINAS"
    },
    "05030012": {
        "Centro Poblado": "CAMILO C - ALTO DE LA VIRGEN"
    },
    "05030013": {
        "Centro Poblado": "PIEDECUESTA - MANI DE LAS CASAS"
    },
    "05031000": {
        "Centro Poblado": "AMALFI"
    },
    "05031004": {
        "Centro Poblado": "PORTACHUELO"
    },
    "05034000": {
        "Centro Poblado": "ANDES"
    },
    "05034001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "05034003": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "05034006": {
        "Centro Poblado": "SANTA RITA"
    },
    "05034007": {
        "Centro Poblado": "TAPARTÓ"
    },
    "05034012": {
        "Centro Poblado": "SANTA INÉS"
    },
    "05034014": {
        "Centro Poblado": "SAN BARTOLO"
    },
    "05034015": {
        "Centro Poblado": "LA CHAPARRALA - LA UNIÓN"
    },
    "05036000": {
        "Centro Poblado": "ANGELÓPOLIS"
    },
    "05036001": {
        "Centro Poblado": "LA ESTACIÓN"
    },
    "05036006": {
        "Centro Poblado": "SANTA RITA"
    },
    "05036011": {
        "Centro Poblado": "CIENAGUITA"
    },
    "05038000": {
        "Centro Poblado": "ANGOSTURA"
    },
    "05038008": {
        "Centro Poblado": "LLANOS DE CUIBA"
    },
    "05040000": {
        "Centro Poblado": "ANORÍ"
    },
    "05040002": {
        "Centro Poblado": "LIBERIA"
    },
    "05042000": {
        "Centro Poblado": "SANTA FÉ DE ANTIOQUIA"
    },
    "05042002": {
        "Centro Poblado": "LAURELES"
    },
    "05042006": {
        "Centro Poblado": "EL PESCADO"
    },
    "05042007": {
        "Centro Poblado": "SABANAS"
    },
    "05042008": {
        "Centro Poblado": "KILOMETRO 2"
    },
    "05042009": {
        "Centro Poblado": "PASO REAL"
    },
    "05044000": {
        "Centro Poblado": "ANZÁ"
    },
    "05044001": {
        "Centro Poblado": "GUINTAR"
    },
    "05044005": {
        "Centro Poblado": "LA CEJITA"
    },
    "05044006": {
        "Centro Poblado": "LA HIGUINA"
    },
    "05045000": {
        "Centro Poblado": "APARTADÓ"
    },
    "05045001": {
        "Centro Poblado": "SAN JOSÉ DE APARTADÓ"
    },
    "05045002": {
        "Centro Poblado": "CHURIDÓ"
    },
    "05045003": {
        "Centro Poblado": "ZUNGO CARRETERA"
    },
    "05045009": {
        "Centro Poblado": "EL REPOSO"
    },
    "05045010": {
        "Centro Poblado": "BAJO DEL OSO"
    },
    "05045011": {
        "Centro Poblado": "EL SALVADOR"
    },
    "05045014": {
        "Centro Poblado": "PUERTO GIRÓN"
    },
    "05045015": {
        "Centro Poblado": "LOMA VERDE"
    },
    "05045016": {
        "Centro Poblado": "SAN PABLO"
    },
    "05045017": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "05045018": {
        "Centro Poblado": "SAL SI PUEDES"
    },
    "05051000": {
        "Centro Poblado": "ARBOLETES"
    },
    "05051001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "05051003": {
        "Centro Poblado": "EL CARMELO"
    },
    "05051005": {
        "Centro Poblado": "LAS NARANJITAS"
    },
    "05051008": {
        "Centro Poblado": "EL YESO"
    },
    "05051009": {
        "Centro Poblado": "LA TRINIDAD"
    },
    "05051010": {
        "Centro Poblado": "LAS PLATAS (SANTAFÉ)"
    },
    "05051011": {
        "Centro Poblado": "LA CANDELARIA"
    },
    "05051014": {
        "Centro Poblado": "EL GUADUAL"
    },
    "05051017": {
        "Centro Poblado": "LA ATOYOSA"
    },
    "05051019": {
        "Centro Poblado": "SAN JOSÉ DEL CARMELO"
    },
    "05055000": {
        "Centro Poblado": "ARGELIA"
    },
    "05059000": {
        "Centro Poblado": "ARMENIA"
    },
    "05059001": {
        "Centro Poblado": "LA HERRADURA"
    },
    "05059003": {
        "Centro Poblado": "EL SOCORRO"
    },
    "05059006": {
        "Centro Poblado": "FILO SECO"
    },
    "05059009": {
        "Centro Poblado": "PALMICHAL"
    },
    "05079000": {
        "Centro Poblado": "BARBOSA"
    },
    "05079001": {
        "Centro Poblado": "HATILLO"
    },
    "05079005": {
        "Centro Poblado": "PLATANITO"
    },
    "05079008": {
        "Centro Poblado": "ISAZA"
    },
    "05079014": {
        "Centro Poblado": "POPALITO"
    },
    "05079016": {
        "Centro Poblado": "YARUMITO"
    },
    "05079017": {
        "Centro Poblado": "TABLAZO - HATILLO"
    },
    "05079018": {
        "Centro Poblado": "EL PARAISO"
    },
    "05079019": {
        "Centro Poblado": "EL SALADITO"
    },
    "05079020": {
        "Centro Poblado": "LOMITA 1"
    },
    "05079021": {
        "Centro Poblado": "LOMITA 2"
    },
    "05079022": {
        "Centro Poblado": "LA PRIMAVERA"
    },
    "05079023": {
        "Centro Poblado": "TAMBORCITO"
    },
    "05086000": {
        "Centro Poblado": "BELMIRA"
    },
    "05086001": {
        "Centro Poblado": "LABORES"
    },
    "05086003": {
        "Centro Poblado": "RÍO ARRIBA"
    },
    "05088000": {
        "Centro Poblado": "BELLO"
    },
    "05088008": {
        "Centro Poblado": "POTRERITO"
    },
    "05088013": {
        "Centro Poblado": "SAN FÉLIX"
    },
    "05088018": {
        "Centro Poblado": "EL PINAR"
    },
    "05088020": {
        "Centro Poblado": "EL ALBERGUE"
    },
    "05088022": {
        "Centro Poblado": "LA CHINA"
    },
    "05088023": {
        "Centro Poblado": "LA UNIÓN"
    },
    "05091000": {
        "Centro Poblado": "BETANIA"
    },
    "05091003": {
        "Centro Poblado": "SAN LUIS"
    },
    "05093000": {
        "Centro Poblado": "BETULIA"
    },
    "05093001": {
        "Centro Poblado": "ALTAMIRA"
    },
    "05101000": {
        "Centro Poblado": "CIUDAD BOLÍVAR"
    },
    "05101002": {
        "Centro Poblado": "SAN BERNARDO DE LOS FARALLONES"
    },
    "05101006": {
        "Centro Poblado": "ALFONSO LÓPEZ (SAN GREGORIO)"
    },
    "05101008": {
        "Centro Poblado": "VILLA ALEGRÍA"
    },
    "05101010": {
        "Centro Poblado": "EL CABRERO - BOLÍVAR ARRIBA"
    },
    "05107000": {
        "Centro Poblado": "BRICEÑO"
    },
    "05107001": {
        "Centro Poblado": "BERLÍN (PUEBLO NUEVO)"
    },
    "05107002": {
        "Centro Poblado": "EL ROBLAL"
    },
    "05107003": {
        "Centro Poblado": "LAS AURAS"
    },
    "05107004": {
        "Centro Poblado": "TRAVESIAS"
    },
    "05113000": {
        "Centro Poblado": "BURITICÁ"
    },
    "05113001": {
        "Centro Poblado": "EL NARANJO"
    },
    "05113002": {
        "Centro Poblado": "GUARCO"
    },
    "05113003": {
        "Centro Poblado": "TABACAL"
    },
    "05113004": {
        "Centro Poblado": "LLANOS DE URARCO"
    },
    "05113005": {
        "Centro Poblado": "LA ANGELINA"
    },
    "05113008": {
        "Centro Poblado": "LA MARIELA"
    },
    "05120000": {
        "Centro Poblado": "CÁCERES"
    },
    "05120002": {
        "Centro Poblado": "EL JARDÍN (TAMANÁ)"
    },
    "05120003": {
        "Centro Poblado": "GUARUMO"
    },
    "05120004": {
        "Centro Poblado": "MANIZALES"
    },
    "05120006": {
        "Centro Poblado": "PUERTO BÉLGICA"
    },
    "05120010": {
        "Centro Poblado": "PIAMONTE"
    },
    "05120012": {
        "Centro Poblado": "RÍO MAN"
    },
    "05120013": {
        "Centro Poblado": "LAS PAMPAS"
    },
    "05120014": {
        "Centro Poblado": "NICARAGUA"
    },
    "05120015": {
        "Centro Poblado": "PUERTO SANTO"
    },
    "05125000": {
        "Centro Poblado": "CAICEDO"
    },
    "05129000": {
        "Centro Poblado": "CALDAS"
    },
    "05129001": {
        "Centro Poblado": "EL CAÑO"
    },
    "05129002": {
        "Centro Poblado": "LA RAYA"
    },
    "05129004": {
        "Centro Poblado": "LA MIEL"
    },
    "05129005": {
        "Centro Poblado": "LA CORRALITA"
    },
    "05129006": {
        "Centro Poblado": "LA PRIMAVERA SANTA CRUZ"
    },
    "05129007": {
        "Centro Poblado": "EL RAIZAL"
    },
    "05129008": {
        "Centro Poblado": "LA CLARA"
    },
    "05129009": {
        "Centro Poblado": "LA QUIEBRA"
    },
    "05129010": {
        "Centro Poblado": "LA SALADA PARTE BAJA"
    },
    "05129011": {
        "Centro Poblado": "LA TOLVA"
    },
    "05129012": {
        "Centro Poblado": "LA VALERIA"
    },
    "05129013": {
        "Centro Poblado": "LA AGUACATALA"
    },
    "05129015": {
        "Centro Poblado": "LA CHUSCALA"
    },
    "05129016": {
        "Centro Poblado": "SALINAS"
    },
    "05134000": {
        "Centro Poblado": "CAMPAMENTO"
    },
    "05134001": {
        "Centro Poblado": "LA CHIQUITA"
    },
    "05134002": {
        "Centro Poblado": "LA SOLITA"
    },
    "05134003": {
        "Centro Poblado": "LLANADAS"
    },
    "05138000": {
        "Centro Poblado": "CAÑASGORDAS"
    },
    "05138001": {
        "Centro Poblado": "BUENOS AIRES - PARTE ALTA"
    },
    "05138002": {
        "Centro Poblado": "CESTILLAL"
    },
    "05138003": {
        "Centro Poblado": "JUNTAS DE URAMITA"
    },
    "05138005": {
        "Centro Poblado": "SAN PASCUAL"
    },
    "05138009": {
        "Centro Poblado": "VILLA VICTORIA"
    },
    "05142000": {
        "Centro Poblado": "CARACOLÍ"
    },
    "05145000": {
        "Centro Poblado": "CARAMANTA"
    },
    "05145001": {
        "Centro Poblado": "ALEGRÍAS"
    },
    "05145002": {
        "Centro Poblado": "SUCRE"
    },
    "05145003": {
        "Centro Poblado": "BARRO BLANCO"
    },
    "05145005": {
        "Centro Poblado": "AGUADITA GRANDE"
    },
    "05145006": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "05147000": {
        "Centro Poblado": "CAREPA"
    },
    "05147003": {
        "Centro Poblado": "PIEDRAS BLANCAS"
    },
    "05147004": {
        "Centro Poblado": "ZUNGO EMBARCADERO - PUEBLO NUEVO"
    },
    "05147005": {
        "Centro Poblado": "ZUNGO EMBARCADERO - 11 DE NOVIEMBRE"
    },
    "05147006": {
        "Centro Poblado": "CASA VERDE"
    },
    "05147007": {
        "Centro Poblado": "EL ENCANTO"
    },
    "05147008": {
        "Centro Poblado": "ZUNGO EMBARCADERO - 28 DE OCTUBRE"
    },
    "05147009": {
        "Centro Poblado": "BELENCITO"
    },
    "05147010": {
        "Centro Poblado": "BOSQUES DE LOS ALMENDROS"
    },
    "05147011": {
        "Centro Poblado": "CAREPITA CANALUNO"
    },
    "05147012": {
        "Centro Poblado": "SACRAMENTO LA LUCHA"
    },
    "05147013": {
        "Centro Poblado": "LOS NARANJALES"
    },
    "05147014": {
        "Centro Poblado": "VIJAGUAL"
    },
    "05147015": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "05148000": {
        "Centro Poblado": "EL CARMEN DE VIBORAL"
    },
    "05148003": {
        "Centro Poblado": "AGUAS CLARAS"
    },
    "05148005": {
        "Centro Poblado": "LA CHAPA"
    },
    "05148006": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "05148008": {
        "Centro Poblado": "LA AURORA - LAS BRISAS"
    },
    "05150000": {
        "Centro Poblado": "CAROLINA DEL PRÍNCIPE"
    },
    "05154000": {
        "Centro Poblado": "CAUCASIA"
    },
    "05154003": {
        "Centro Poblado": "CUTURÚ"
    },
    "05154006": {
        "Centro Poblado": "MARGENTO"
    },
    "05154007": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "05154008": {
        "Centro Poblado": "PALANCA"
    },
    "05154009": {
        "Centro Poblado": "PALOMAR"
    },
    "05154012": {
        "Centro Poblado": "SANTA ROSITA"
    },
    "05154020": {
        "Centro Poblado": "PUERTO TRIANA"
    },
    "05154022": {
        "Centro Poblado": "LA ILUSIÓN"
    },
    "05154023": {
        "Centro Poblado": "CACERÍ"
    },
    "05154024": {
        "Centro Poblado": "EL PANDO"
    },
    "05154026": {
        "Centro Poblado": "EL CHINO"
    },
    "05154027": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "05154031": {
        "Centro Poblado": "VILLA DEL SOCORRO"
    },
    "05154032": {
        "Centro Poblado": "CASERÍO CONJUNTO CAÑA FISTULA"
    },
    "05154033": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "05172000": {
        "Centro Poblado": "CHIGORODÓ"
    },
    "05172003": {
        "Centro Poblado": "BARRANQUILLITA"
    },
    "05172007": {
        "Centro Poblado": "GUAPÁ CARRETERAS"
    },
    "05172013": {
        "Centro Poblado": "JURADÓ"
    },
    "05172014": {
        "Centro Poblado": "CAMPITAS"
    },
    "05172015": {
        "Centro Poblado": "CHAMPITA SECTOR LA GRANJA"
    },
    "05190000": {
        "Centro Poblado": "CISNEROS"
    },
    "05197000": {
        "Centro Poblado": "COCORNÁ"
    },
    "05197005": {
        "Centro Poblado": "LA PIÑUELA"
    },
    "05197013": {
        "Centro Poblado": "EL MOLINO"
    },
    "05206000": {
        "Centro Poblado": "CONCEPCIÓN"
    },
    "05209000": {
        "Centro Poblado": "CONCORDIA"
    },
    "05209001": {
        "Centro Poblado": "EL SOCORRO"
    },
    "05209006": {
        "Centro Poblado": "EL GOLPE"
    },
    "05209007": {
        "Centro Poblado": "SALAZAR"
    },
    "05212000": {
        "Centro Poblado": "COPACABANA"
    },
    "05212005": {
        "Centro Poblado": "EL SALADO"
    },
    "05212008": {
        "Centro Poblado": "CABUYAL"
    },
    "05212017": {
        "Centro Poblado": "EL LLANO"
    },
    "05234000": {
        "Centro Poblado": "DABEIBA"
    },
    "05234004": {
        "Centro Poblado": "SAN JOSÉ DE URAMA"
    },
    "05234008": {
        "Centro Poblado": "ARMENIA - CAMPARRUSIA"
    },
    "05234010": {
        "Centro Poblado": "LAS CRUCES DE URAMA"
    },
    "05234012": {
        "Centro Poblado": "CHIMIADÓ LLANO GRANDE"
    },
    "05234014": {
        "Centro Poblado": "EL BOTÓN"
    },
    "05234017": {
        "Centro Poblado": "BETANIA PUENTE NUEVO"
    },
    "05234018": {
        "Centro Poblado": "CARA COLÓN"
    },
    "05234019": {
        "Centro Poblado": "LA BALSITA"
    },
    "05237000": {
        "Centro Poblado": "DONMATÍAS"
    },
    "05237001": {
        "Centro Poblado": "BELLAVISTA"
    },
    "05237003": {
        "Centro Poblado": "ARENALES"
    },
    "05237004": {
        "Centro Poblado": "MONTERA"
    },
    "05237005": {
        "Centro Poblado": "PRADERA"
    },
    "05240000": {
        "Centro Poblado": "EBÉJICO"
    },
    "05240001": {
        "Centro Poblado": "BRASIL"
    },
    "05240003": {
        "Centro Poblado": "SEVILLA"
    },
    "05240008": {
        "Centro Poblado": "EL ZARZAL"
    },
    "05240011": {
        "Centro Poblado": "LA CLARA"
    },
    "05240012": {
        "Centro Poblado": "FATIMA"
    },
    "05250000": {
        "Centro Poblado": "EL BAGRE"
    },
    "05250002": {
        "Centro Poblado": "PUERTO CLAVER"
    },
    "05250004": {
        "Centro Poblado": "PUERTO LÓPEZ"
    },
    "05250005": {
        "Centro Poblado": "EL REAL"
    },
    "05250006": {
        "Centro Poblado": "LA CORONA"
    },
    "05250007": {
        "Centro Poblado": "LAS NEGRITAS"
    },
    "05250008": {
        "Centro Poblado": "LAS SARDINAS EL PUENTE"
    },
    "05250009": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "05250010": {
        "Centro Poblado": "MUQUI"
    },
    "05250011": {
        "Centro Poblado": "BORRACHERA"
    },
    "05250012": {
        "Centro Poblado": "CAÑO CLARO"
    },
    "05250013": {
        "Centro Poblado": "LOS ALMENDROS"
    },
    "05264000": {
        "Centro Poblado": "ENTRERRÍOS"
    },
    "05266000": {
        "Centro Poblado": "ENVIGADO"
    },
    "05266001": {
        "Centro Poblado": "LAS PALMAS"
    },
    "05266005": {
        "Centro Poblado": "EL CRISTO"
    },
    "05266006": {
        "Centro Poblado": "EL CHINGUI  2"
    },
    "05266007": {
        "Centro Poblado": "LA ÚLTIMA COPA"
    },
    "05266008": {
        "Centro Poblado": "PARCELACIÓN LA ACUARELA"
    },
    "05266009": {
        "Centro Poblado": "PARCELACIÓN ALAMOS DEL ESCOBERO"
    },
    "05266010": {
        "Centro Poblado": "PARCELACIÓN ALDEA DE PALMA VERDE"
    },
    "05266011": {
        "Centro Poblado": "PARCELACIÓN CONDOMINIO CAMPESTRE SERRANÍA"
    },
    "05266012": {
        "Centro Poblado": "PARCELACIÓN CASAS BELLO MONTE"
    },
    "05266013": {
        "Centro Poblado": "PARCELACIÓN FIORE CASAS DE CAMPO"
    },
    "05266014": {
        "Centro Poblado": "PARCELACIÓN CONJUNTO RESIDENCIAL BELLA TIERRA"
    },
    "05266015": {
        "Centro Poblado": "PARCELACIÓN ENCENILLOS"
    },
    "05266016": {
        "Centro Poblado": "PARCELACIÓN ESCOBERO"
    },
    "05266017": {
        "Centro Poblado": "PARCELACIÓN HACIENDA ARRAYANES"
    },
    "05266018": {
        "Centro Poblado": "PARCELACIÓN LAS PALMITAS"
    },
    "05266019": {
        "Centro Poblado": "PARCELACIÓN LEMONT"
    },
    "05266020": {
        "Centro Poblado": "PARCELACIÓN PRADO LARGO"
    },
    "05266021": {
        "Centro Poblado": "PARCELACIÓN SAN SEBASTIÁN"
    },
    "05266023": {
        "Centro Poblado": "PARCELACIÓN URBANIZACIÓN PAPIROS"
    },
    "05266024": {
        "Centro Poblado": "PARCELACIÓN VERANDA"
    },
    "05266025": {
        "Centro Poblado": "PARCELACIÓN VILLAS DE LA CANDELARIA"
    },
    "05282000": {
        "Centro Poblado": "FREDONIA"
    },
    "05282002": {
        "Centro Poblado": "LOS PALOMOS"
    },
    "05282003": {
        "Centro Poblado": "MINAS"
    },
    "05282004": {
        "Centro Poblado": "PUENTE IGLESIAS"
    },
    "05282005": {
        "Centro Poblado": "MARSELLA"
    },
    "05282008": {
        "Centro Poblado": "EL ZANCUDO"
    },
    "05284000": {
        "Centro Poblado": "FRONTINO"
    },
    "05284001": {
        "Centro Poblado": "CARAUTA"
    },
    "05284004": {
        "Centro Poblado": "MURRI - LA BLANQUITA"
    },
    "05284005": {
        "Centro Poblado": "MUSINGA - TABLADITO"
    },
    "05284006": {
        "Centro Poblado": "NUTIBARA"
    },
    "05284007": {
        "Centro Poblado": "PONTÓN"
    },
    "05284010": {
        "Centro Poblado": "SAN LAZARO"
    },
    "05306000": {
        "Centro Poblado": "GIRALDO"
    },
    "05306001": {
        "Centro Poblado": "MANGLAR"
    },
    "05308000": {
        "Centro Poblado": "GIRARDOTA"
    },
    "05308002": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "05308004": {
        "Centro Poblado": "LA PALMA"
    },
    "05308009": {
        "Centro Poblado": "CABILDO"
    },
    "05308010": {
        "Centro Poblado": "LAS CUCHILLAS"
    },
    "05308011": {
        "Centro Poblado": "JAMUNDÍ - ESCUELAS"
    },
    "05308012": {
        "Centro Poblado": "JUAN COJO"
    },
    "05308013": {
        "Centro Poblado": "LA CALLE"
    },
    "05308014": {
        "Centro Poblado": "SAN ESTEBAN"
    },
    "05308015": {
        "Centro Poblado": "EL PARAISO"
    },
    "05308016": {
        "Centro Poblado": "JAMUNDÍ - RIELES"
    },
    "05308017": {
        "Centro Poblado": "LOMA DE LOS OCHOA"
    },
    "05310000": {
        "Centro Poblado": "GÓMEZ PLATA"
    },
    "05310001": {
        "Centro Poblado": "EL SALTO"
    },
    "05310002": {
        "Centro Poblado": "SAN MATÍAS"
    },
    "05310004": {
        "Centro Poblado": "VEGA DE BOTERO"
    },
    "05313000": {
        "Centro Poblado": "GRANADA"
    },
    "05313001": {
        "Centro Poblado": "SANTA ANA"
    },
    "05313004": {
        "Centro Poblado": "LOS MEDIOS"
    },
    "05315000": {
        "Centro Poblado": "GUADALUPE"
    },
    "05315002": {
        "Centro Poblado": "GUANTEROS"
    },
    "05315007": {
        "Centro Poblado": "GUADALUPE IV"
    },
    "05315008": {
        "Centro Poblado": "BARRIO NUEVO"
    },
    "05315009": {
        "Centro Poblado": "EL MACHETE"
    },
    "05318000": {
        "Centro Poblado": "GUARNE"
    },
    "05318006": {
        "Centro Poblado": "CHAPARRAL"
    },
    "05318007": {
        "Centro Poblado": "SAN IGNACIO"
    },
    "05321000": {
        "Centro Poblado": "GUATAPÉ"
    },
    "05321001": {
        "Centro Poblado": "EL ROBLE"
    },
    "05347000": {
        "Centro Poblado": "HELICONIA"
    },
    "05347001": {
        "Centro Poblado": "ALTO DEL CORRAL"
    },
    "05347002": {
        "Centro Poblado": "PUEBLITO"
    },
    "05347003": {
        "Centro Poblado": "LLANOS DE SAN JOSÉ"
    },
    "05347009": {
        "Centro Poblado": "GUAMAL"
    },
    "05353000": {
        "Centro Poblado": "HISPANIA"
    },
    "05360000": {
        "Centro Poblado": "ITAGÜÍ"
    },
    "05360001": {
        "Centro Poblado": "LOS GÓMEZ"
    },
    "05360003": {
        "Centro Poblado": "EL AJIZAL"
    },
    "05360006": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "05360012": {
        "Centro Poblado": "EL PORVENIR"
    },
    "05360013": {
        "Centro Poblado": "EL PROGRESO"
    },
    "05360014": {
        "Centro Poblado": "LA MARÍA"
    },
    "05361000": {
        "Centro Poblado": "ITUANGO"
    },
    "05361002": {
        "Centro Poblado": "EL ARO - BUILÓPOLIS"
    },
    "05361003": {
        "Centro Poblado": "LA GRANJA"
    },
    "05361004": {
        "Centro Poblado": "PASCUITA"
    },
    "05361005": {
        "Centro Poblado": "SANTA ANA"
    },
    "05361006": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "05361007": {
        "Centro Poblado": "SANTA RITA"
    },
    "05361018": {
        "Centro Poblado": "PÍO X"
    },
    "05364000": {
        "Centro Poblado": "JARDÍN"
    },
    "05364001": {
        "Centro Poblado": "CRISTIANÍA"
    },
    "05364002": {
        "Centro Poblado": "LA ARBOLEDA - LAS MACANAS"
    },
    "05364006": {
        "Centro Poblado": "QUEBRADA BONITA"
    },
    "05368000": {
        "Centro Poblado": "JERICÓ"
    },
    "05368005": {
        "Centro Poblado": "GUACAMAYAL"
    },
    "05368007": {
        "Centro Poblado": "LOS PATIOS"
    },
    "05376000": {
        "Centro Poblado": "LA CEJA"
    },
    "05376002": {
        "Centro Poblado": "EL TAMBO"
    },
    "05376003": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "05376005": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "05376006": {
        "Centro Poblado": "SAN JUDAS"
    },
    "05376008": {
        "Centro Poblado": "TOLEDO"
    },
    "05380000": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "05380007": {
        "Centro Poblado": "LA TABLACITA"
    },
    "05380008": {
        "Centro Poblado": "SAGRADA FAMILIA"
    },
    "05380009": {
        "Centro Poblado": "SAN JOSÉ - MELEGUINDO"
    },
    "05380010": {
        "Centro Poblado": "LA RAYA"
    },
    "05380011": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "05380012": {
        "Centro Poblado": "TARAPACÁ"
    },
    "05380013": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "05380019": {
        "Centro Poblado": "LA BERMEJALA"
    },
    "05380020": {
        "Centro Poblado": "PAN DE AZÚCAR"
    },
    "05380021": {
        "Centro Poblado": "PEÑAS BLANCAS"
    },
    "05390000": {
        "Centro Poblado": "LA PINTADA"
    },
    "05390001": {
        "Centro Poblado": "LA BOCANA"
    },
    "05400000": {
        "Centro Poblado": "LA UNIÓN"
    },
    "05400001": {
        "Centro Poblado": "MESOPOTAMIA"
    },
    "05400004": {
        "Centro Poblado": "LA CONCHA"
    },
    "05411000": {
        "Centro Poblado": "LIBORINA"
    },
    "05411001": {
        "Centro Poblado": "EL CARMEN - LA VENTA"
    },
    "05411002": {
        "Centro Poblado": "LA HONDA"
    },
    "05411003": {
        "Centro Poblado": "LA MERCED (PLAYÓN)"
    },
    "05411004": {
        "Centro Poblado": "SAN DIEGO (PLACITA)"
    },
    "05411005": {
        "Centro Poblado": "CURITÍ"
    },
    "05411007": {
        "Centro Poblado": "CRISTÓBAL"
    },
    "05411012": {
        "Centro Poblado": "PORVENIR"
    },
    "05411013": {
        "Centro Poblado": "PROVINCIAL"
    },
    "05425000": {
        "Centro Poblado": "MACEO"
    },
    "05425001": {
        "Centro Poblado": "LA SUSANA"
    },
    "05425003": {
        "Centro Poblado": "LA FLORESTA"
    },
    "05425005": {
        "Centro Poblado": "SAN JOSÉ DEL NUS (JOSÉ DE NUESTRA SEÑORA)"
    },
    "05440000": {
        "Centro Poblado": "MARINILLA"
    },
    "05467000": {
        "Centro Poblado": "MONTEBELLO"
    },
    "05467001": {
        "Centro Poblado": "SABALETAS"
    },
    "05467006": {
        "Centro Poblado": "LA GRANJA"
    },
    "05467008": {
        "Centro Poblado": "PIEDRA GALANA"
    },
    "05475000": {
        "Centro Poblado": "MURINDÓ"
    },
    "05475001": {
        "Centro Poblado": "OPOGADO"
    },
    "05475005": {
        "Centro Poblado": "JEDEGA"
    },
    "05475006": {
        "Centro Poblado": "TADÍA"
    },
    "05475007": {
        "Centro Poblado": "BEBARAMEÑO"
    },
    "05480000": {
        "Centro Poblado": "MUTATÁ"
    },
    "05480001": {
        "Centro Poblado": "BEJUQUILLO"
    },
    "05480002": {
        "Centro Poblado": "PAVARANDOCITO"
    },
    "05480003": {
        "Centro Poblado": "VILLA ARTEAGA"
    },
    "05480004": {
        "Centro Poblado": "PAVARANDO GRANDE"
    },
    "05480006": {
        "Centro Poblado": "CAUCHERAS"
    },
    "05483000": {
        "Centro Poblado": "NARIÑO"
    },
    "05483001": {
        "Centro Poblado": "PUERTO VENUS"
    },
    "05490000": {
        "Centro Poblado": "NECOCLÍ"
    },
    "05490001": {
        "Centro Poblado": "EL TOTUMO"
    },
    "05490002": {
        "Centro Poblado": "MULATOS"
    },
    "05490003": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "05490004": {
        "Centro Poblado": "ZAPATA"
    },
    "05490005": {
        "Centro Poblado": "CARIBIA"
    },
    "05490006": {
        "Centro Poblado": "VEREDA CASA BLANCA"
    },
    "05490007": {
        "Centro Poblado": "VEREDA EL BOBAL"
    },
    "05490008": {
        "Centro Poblado": "LAS CHANGAS"
    },
    "05490009": {
        "Centro Poblado": "EL MELLITO"
    },
    "05490010": {
        "Centro Poblado": "BRISAS DEL RÍO"
    },
    "05490011": {
        "Centro Poblado": "CARLOS ARRIBA"
    },
    "05490012": {
        "Centro Poblado": "EL VOLAO"
    },
    "05490013": {
        "Centro Poblado": "LA COMARCA"
    },
    "05490014": {
        "Centro Poblado": "LOMA DE PIEDRA"
    },
    "05490015": {
        "Centro Poblado": "MELLO VILLAVICENCIO"
    },
    "05490016": {
        "Centro Poblado": "TULAPITA"
    },
    "05490018": {
        "Centro Poblado": "VALE PAVA"
    },
    "05495000": {
        "Centro Poblado": "NECHÍ"
    },
    "05495001": {
        "Centro Poblado": "BIJAGUAL"
    },
    "05495002": {
        "Centro Poblado": "COLORADO"
    },
    "05495003": {
        "Centro Poblado": "LA CONCHA"
    },
    "05495004": {
        "Centro Poblado": "LAS FLORES"
    },
    "05495005": {
        "Centro Poblado": "CARGUEROS"
    },
    "05495006": {
        "Centro Poblado": "PUERTO ASTILLA"
    },
    "05501000": {
        "Centro Poblado": "OLAYA"
    },
    "05501001": {
        "Centro Poblado": "LLANADAS"
    },
    "05501002": {
        "Centro Poblado": "SUCRE"
    },
    "05501004": {
        "Centro Poblado": "QUEBRADA SECA"
    },
    "05541000": {
        "Centro Poblado": "PEÑOL"
    },
    "05543000": {
        "Centro Poblado": "PEQUE"
    },
    "05543003": {
        "Centro Poblado": "LOS LLANOS"
    },
    "05576000": {
        "Centro Poblado": "PUEBLORRICO"
    },
    "05579000": {
        "Centro Poblado": "PUERTO BERRÍO"
    },
    "05579001": {
        "Centro Poblado": "PUERTO MURILLO"
    },
    "05579002": {
        "Centro Poblado": "VIRGINIAS"
    },
    "05579003": {
        "Centro Poblado": "CABAÑAS"
    },
    "05579004": {
        "Centro Poblado": "EL BRASIL"
    },
    "05579005": {
        "Centro Poblado": "LA CRISTALINA"
    },
    "05579009": {
        "Centro Poblado": "MALENA"
    },
    "05579010": {
        "Centro Poblado": "CALERA"
    },
    "05579011": {
        "Centro Poblado": "BODEGAS"
    },
    "05579012": {
        "Centro Poblado": "DORADO - CALAMAR"
    },
    "05579013": {
        "Centro Poblado": "LA CARLOTA"
    },
    "05579014": {
        "Centro Poblado": "MINAS DEL VAPOR"
    },
    "05579015": {
        "Centro Poblado": "SANTA MARTINA"
    },
    "05585000": {
        "Centro Poblado": "PUERTO NARE"
    },
    "05585001": {
        "Centro Poblado": "ARABIA"
    },
    "05585002": {
        "Centro Poblado": "LOS DELIRIOS"
    },
    "05585003": {
        "Centro Poblado": "LA SIERRA"
    },
    "05585004": {
        "Centro Poblado": "LA UNIÓN"
    },
    "05585006": {
        "Centro Poblado": "LA PESCA"
    },
    "05585008": {
        "Centro Poblado": "LAS ANGELITAS"
    },
    "05585009": {
        "Centro Poblado": "LA CLARA"
    },
    "05585010": {
        "Centro Poblado": "EL PRODIGIO"
    },
    "05591000": {
        "Centro Poblado": "PUERTO TRIUNFO"
    },
    "05591002": {
        "Centro Poblado": "PUERTO PERALES NUEVO"
    },
    "05591003": {
        "Centro Poblado": "ESTACIÓN COCORNÁ"
    },
    "05591004": {
        "Centro Poblado": "DORADAL"
    },
    "05591005": {
        "Centro Poblado": "LA MERCEDES"
    },
    "05591007": {
        "Centro Poblado": "ESTACIÓN PITA"
    },
    "05591008": {
        "Centro Poblado": "LA FLORIDA"
    },
    "05591009": {
        "Centro Poblado": "SANTIAGO BERRIO"
    },
    "05591011": {
        "Centro Poblado": "TRES RANCHOS"
    },
    "05604000": {
        "Centro Poblado": "REMEDIOS"
    },
    "05604001": {
        "Centro Poblado": "LA CRUZADA"
    },
    "05604003": {
        "Centro Poblado": "SANTA ISABEL"
    },
    "05604005": {
        "Centro Poblado": "OTÚ"
    },
    "05604007": {
        "Centro Poblado": "CAÑAVERAL"
    },
    "05604008": {
        "Centro Poblado": "MARTANA"
    },
    "05604009": {
        "Centro Poblado": "RÍO BAGRE"
    },
    "05604010": {
        "Centro Poblado": "CAMPO VIJAO"
    },
    "05607000": {
        "Centro Poblado": "RETIRO"
    },
    "05607003": {
        "Centro Poblado": "ALTO DE CARRIZALES"
    },
    "05607004": {
        "Centro Poblado": "DON DIEGO"
    },
    "05607005": {
        "Centro Poblado": "EL CHUSCAL LA CAMPANITA"
    },
    "05607007": {
        "Centro Poblado": "LOS SALADOS"
    },
    "05607009": {
        "Centro Poblado": "EL PORTENTO"
    },
    "05607013": {
        "Centro Poblado": "CARRIZALES LA BORRASCOSA"
    },
    "05615000": {
        "Centro Poblado": "RIONEGRO"
    },
    "05615002": {
        "Centro Poblado": "EL TABLAZO"
    },
    "05615009": {
        "Centro Poblado": "CABECERAS DE LLANO GRANDE"
    },
    "05615013": {
        "Centro Poblado": "PONTEZUELA"
    },
    "05615014": {
        "Centro Poblado": "ALTO BONITO"
    },
    "05615017": {
        "Centro Poblado": "LA MOSCA"
    },
    "05615025": {
        "Centro Poblado": "BARRO BLANCO"
    },
    "05615026": {
        "Centro Poblado": "CONDOMINIO CAMPESTRE LAGO GRANDE"
    },
    "05615027": {
        "Centro Poblado": "CONDOMINIO EL REMANSO"
    },
    "05615028": {
        "Centro Poblado": "CONDOMINIO SIERRAS DE MAYORI"
    },
    "05615029": {
        "Centro Poblado": "CONDOMINIO VILLAS DE LLANO GRANDE"
    },
    "05615030": {
        "Centro Poblado": "GALICIA PARTE ALTA"
    },
    "05615031": {
        "Centro Poblado": "GALICIA PARTE BAJA"
    },
    "05615032": {
        "Centro Poblado": "JAMAICA PARCELACION CAMPESTRE"
    },
    "05615033": {
        "Centro Poblado": "PARCELACIÓN AGUA LUNA DE ORIENTE"
    },
    "05615034": {
        "Centro Poblado": "PARCELACION ANDALUCIA"
    },
    "05615035": {
        "Centro Poblado": "PARCELACION CAMELOT"
    },
    "05615036": {
        "Centro Poblado": "PARCELACIÓN COCUYO"
    },
    "05615037": {
        "Centro Poblado": "PARCELACIÓN COLINAS DE PAIMADÓ"
    },
    "05615039": {
        "Centro Poblado": "PARCELACIÓN LA QUERENCIA"
    },
    "05615043": {
        "Centro Poblado": "PARCELACION SANTA MARIA DEL LLANO"
    },
    "05615045": {
        "Centro Poblado": "PARCELACIÓN TORRE MOLINOS"
    },
    "05615046": {
        "Centro Poblado": "PARCELACIÓN TOSCANA"
    },
    "05615047": {
        "Centro Poblado": "PARCELACIÓN VEGAS DE GUADALCANAL"
    },
    "05615048": {
        "Centro Poblado": "ABREITO"
    },
    "05628000": {
        "Centro Poblado": "SABANALARGA"
    },
    "05628001": {
        "Centro Poblado": "EL JUNCO"
    },
    "05628002": {
        "Centro Poblado": "EL ORO"
    },
    "05628004": {
        "Centro Poblado": "EL SOCORRO"
    },
    "05628007": {
        "Centro Poblado": "MEMBRILLAL"
    },
    "05631000": {
        "Centro Poblado": "SABANETA"
    },
    "05631001": {
        "Centro Poblado": "MARÍA AUXILIADORA"
    },
    "05631002": {
        "Centro Poblado": "CAÑAVERALEJO"
    },
    "05631006": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "05631007": {
        "Centro Poblado": "LA INMACULADA"
    },
    "05631009": {
        "Centro Poblado": "LA DOCTORA"
    },
    "05631010": {
        "Centro Poblado": "LAS LOMITAS"
    },
    "05631013": {
        "Centro Poblado": "LOMA DE LOS HENAO"
    },
    "05642000": {
        "Centro Poblado": "SALGAR"
    },
    "05642001": {
        "Centro Poblado": "EL CONCILIO"
    },
    "05642002": {
        "Centro Poblado": "LA CÁMARA"
    },
    "05642003": {
        "Centro Poblado": "LA MARGARITA"
    },
    "05642010": {
        "Centro Poblado": "PEÑALISA"
    },
    "05647000": {
        "Centro Poblado": "SAN ANDRÉS DE CUERQUÍA"
    },
    "05649000": {
        "Centro Poblado": "SAN CARLOS"
    },
    "05649001": {
        "Centro Poblado": "EL JORDÁN"
    },
    "05649002": {
        "Centro Poblado": "SAMANÁ"
    },
    "05649005": {
        "Centro Poblado": "PUERTO GARZA"
    },
    "05649012": {
        "Centro Poblado": "DOS QUEBRADAS"
    },
    "05649013": {
        "Centro Poblado": "LA HONDITA"
    },
    "05649014": {
        "Centro Poblado": "VALLEJUELO"
    },
    "05652000": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "05652001": {
        "Centro Poblado": "AQUITANIA"
    },
    "05652008": {
        "Centro Poblado": "PAILANIA"
    },
    "05652010": {
        "Centro Poblado": "RÍO CLARO"
    },
    "05656000": {
        "Centro Poblado": "SAN JERÓNIMO"
    },
    "05658000": {
        "Centro Poblado": "SAN JOSÉ DE LA MONTAÑA"
    },
    "05659000": {
        "Centro Poblado": "SAN JUAN DE URABÁ"
    },
    "05659001": {
        "Centro Poblado": "DAMAQUIEL"
    },
    "05659002": {
        "Centro Poblado": "SAN JUANCITO"
    },
    "05659003": {
        "Centro Poblado": "UVEROS"
    },
    "05659004": {
        "Centro Poblado": "SIETE VUELTAS"
    },
    "05659005": {
        "Centro Poblado": "SAN NICOLÁS DEL RÍO"
    },
    "05659006": {
        "Centro Poblado": "BALSILLA"
    },
    "05659007": {
        "Centro Poblado": "CALLE LARGA"
    },
    "05659008": {
        "Centro Poblado": "MONTECRISTO"
    },
    "05660000": {
        "Centro Poblado": "SAN LUIS"
    },
    "05660001": {
        "Centro Poblado": "EL SILENCIO PERLA VERDE"
    },
    "05660007": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "05660011": {
        "Centro Poblado": "MONTELORO (LA JOSEFINA)"
    },
    "05660012": {
        "Centro Poblado": "LA TEBAIDA"
    },
    "05660013": {
        "Centro Poblado": "SOPETRÁN"
    },
    "05660014": {
        "Centro Poblado": "EL SILENCIO - EL VENTIADERO"
    },
    "05664000": {
        "Centro Poblado": "SAN PEDRO DE LOS MILAGROS"
    },
    "05664005": {
        "Centro Poblado": "OVEJAS"
    },
    "05665000": {
        "Centro Poblado": "SAN PEDRO DE URABÁ"
    },
    "05665002": {
        "Centro Poblado": "SANTA CATALINA"
    },
    "05665003": {
        "Centro Poblado": "ARENAS MONAS"
    },
    "05665004": {
        "Centro Poblado": "ZAPINDONGA"
    },
    "05665008": {
        "Centro Poblado": "EL TOMATE"
    },
    "05665014": {
        "Centro Poblado": "EL CERRITO"
    },
    "05667000": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "05670000": {
        "Centro Poblado": "SAN ROQUE"
    },
    "05670001": {
        "Centro Poblado": "CRISTALES"
    },
    "05670002": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "05670003": {
        "Centro Poblado": "SAN JOSÉ DEL NUS"
    },
    "05674000": {
        "Centro Poblado": "SAN VICENTE"
    },
    "05674001": {
        "Centro Poblado": "CORRIENTES"
    },
    "05679000": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "05679001": {
        "Centro Poblado": "DAMASCO"
    },
    "05679004": {
        "Centro Poblado": "VERSALLES"
    },
    "05679009": {
        "Centro Poblado": "YARUMALITO"
    },
    "05679010": {
        "Centro Poblado": "LA LIBORIANA"
    },
    "05679011": {
        "Centro Poblado": "ZARCITOS PARTE ALTA"
    },
    "05686000": {
        "Centro Poblado": "SANTA ROSA DE OSOS"
    },
    "05686001": {
        "Centro Poblado": "ARAGÓN"
    },
    "05686003": {
        "Centro Poblado": "HOYORRICO"
    },
    "05686004": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "05686006": {
        "Centro Poblado": "SAN PABLO"
    },
    "05686008": {
        "Centro Poblado": "RÍO GRANDE"
    },
    "05690000": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "05690001": {
        "Centro Poblado": "BOTERO"
    },
    "05690003": {
        "Centro Poblado": "PORCECITO"
    },
    "05690004": {
        "Centro Poblado": "SANTIAGO"
    },
    "05690005": {
        "Centro Poblado": "VERSALLES"
    },
    "05697000": {
        "Centro Poblado": "EL SANTUARIO"
    },
    "05736000": {
        "Centro Poblado": "SEGOVIA"
    },
    "05736001": {
        "Centro Poblado": "FRAGUAS"
    },
    "05736002": {
        "Centro Poblado": "PUERTO CALAVERA"
    },
    "05736003": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "05736006": {
        "Centro Poblado": "EL CHISPERO"
    },
    "05736008": {
        "Centro Poblado": "CARRIZAL"
    },
    "05756000": {
        "Centro Poblado": "SONSÓN"
    },
    "05756001": {
        "Centro Poblado": "ALTO DE SABANAS"
    },
    "05756005": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "05756030": {
        "Centro Poblado": "LA DANTA"
    },
    "05756033": {
        "Centro Poblado": "JERUSALÉN"
    },
    "05756034": {
        "Centro Poblado": "EL ALTO DEL POLLO"
    },
    "05761000": {
        "Centro Poblado": "SOPETRÁN"
    },
    "05761001": {
        "Centro Poblado": "CÓRDOBA"
    },
    "05761003": {
        "Centro Poblado": "HORIZONTES"
    },
    "05761005": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "05761011": {
        "Centro Poblado": "LA MIRANDA"
    },
    "05761012": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "05789000": {
        "Centro Poblado": "TÁMESIS"
    },
    "05789001": {
        "Centro Poblado": "PALERMO"
    },
    "05789002": {
        "Centro Poblado": "SAN PABLO"
    },
    "05790000": {
        "Centro Poblado": "TARAZÁ"
    },
    "05790001": {
        "Centro Poblado": "BARRO BLANCO"
    },
    "05790002": {
        "Centro Poblado": "EL DOCE"
    },
    "05790003": {
        "Centro Poblado": "PUERTO ANTIOQUIA"
    },
    "05790004": {
        "Centro Poblado": "LA CAUCANA"
    },
    "05790005": {
        "Centro Poblado": "EL GUAIMARO"
    },
    "05790006": {
        "Centro Poblado": "PIEDRAS"
    },
    "05792000": {
        "Centro Poblado": "TARSO"
    },
    "05792003": {
        "Centro Poblado": "TOCA MOCHO"
    },
    "05792006": {
        "Centro Poblado": "EL CEDRÓN"
    },
    "05809000": {
        "Centro Poblado": "TITIRIBÍ"
    },
    "05809001": {
        "Centro Poblado": "LA MESETA"
    },
    "05809002": {
        "Centro Poblado": "ALBANIA"
    },
    "05809003": {
        "Centro Poblado": "OTRAMINA"
    },
    "05809004": {
        "Centro Poblado": "SITIO VIEJO"
    },
    "05809014": {
        "Centro Poblado": "PORVENIR"
    },
    "05809016": {
        "Centro Poblado": "PUERTO ESCONDIDO"
    },
    "05809018": {
        "Centro Poblado": "VOLCÁN"
    },
    "05819000": {
        "Centro Poblado": "TOLEDO"
    },
    "05819001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "05819002": {
        "Centro Poblado": "EL VALLE"
    },
    "05819005": {
        "Centro Poblado": "EL BRUGO"
    },
    "05837000": {
        "Centro Poblado": "TURBO, DISTRITO PORTUARIO, LOGÍSTICO, INDUSTRIAL, TURÍSTICO Y COMERCIAL"
    },
    "05837001": {
        "Centro Poblado": "CURRULAO"
    },
    "05837002": {
        "Centro Poblado": "NUEVA COLONIA"
    },
    "05837003": {
        "Centro Poblado": "EL TRES"
    },
    "05837005": {
        "Centro Poblado": "SAN VICENTE DEL CONGO"
    },
    "05837006": {
        "Centro Poblado": "TIE"
    },
    "05837007": {
        "Centro Poblado": "LOMAS AISLADAS"
    },
    "05837008": {
        "Centro Poblado": "RÍO GRANDE"
    },
    "05837009": {
        "Centro Poblado": "BOCAS DEL RÍO ATRATO"
    },
    "05837010": {
        "Centro Poblado": "EL DOS"
    },
    "05837012": {
        "Centro Poblado": "PUEBLO BELLO"
    },
    "05837013": {
        "Centro Poblado": "SAN JOSÉ DE MULATOS"
    },
    "05837014": {
        "Centro Poblado": "PUERTO RICO"
    },
    "05837018": {
        "Centro Poblado": "NUEVO ANTIOQUIA"
    },
    "05837020": {
        "Centro Poblado": "ALTO DE MULATOS"
    },
    "05837023": {
        "Centro Poblado": "CASANOVA"
    },
    "05837024": {
        "Centro Poblado": "LAS GARZAS"
    },
    "05837025": {
        "Centro Poblado": "VILLA MARÍA"
    },
    "05837026": {
        "Centro Poblado": "CODELSA"
    },
    "05837027": {
        "Centro Poblado": "EL PORVENIR"
    },
    "05837028": {
        "Centro Poblado": "NUEVA GRANADA"
    },
    "05837029": {
        "Centro Poblado": "PUNTA DE PIEDRA"
    },
    "05837030": {
        "Centro Poblado": "AMSTERCOL I"
    },
    "05837031": {
        "Centro Poblado": "AMSTERCOL II"
    },
    "05837032": {
        "Centro Poblado": "CIRILO"
    },
    "05837033": {
        "Centro Poblado": "CONGO ARRIBA"
    },
    "05837034": {
        "Centro Poblado": "EL UNO"
    },
    "05837035": {
        "Centro Poblado": "GUADUALITO"
    },
    "05837036": {
        "Centro Poblado": "LAS BABILLAS"
    },
    "05837037": {
        "Centro Poblado": "LOS ENAMORADOS"
    },
    "05837038": {
        "Centro Poblado": "MAKENCAL"
    },
    "05837039": {
        "Centro Poblado": "PIEDRECITAS"
    },
    "05837040": {
        "Centro Poblado": "SANTIAGO DE URABA"
    },
    "05837041": {
        "Centro Poblado": "SIETE DE AGOSTO"
    },
    "05837042": {
        "Centro Poblado": "SINAI"
    },
    "05837043": {
        "Centro Poblado": "EL ROTO"
    },
    "05842000": {
        "Centro Poblado": "URAMITA"
    },
    "05842003": {
        "Centro Poblado": "EL PITAL"
    },
    "05842004": {
        "Centro Poblado": "EL MADERO"
    },
    "05842005": {
        "Centro Poblado": "LIMÓN CHUPADERO"
    },
    "05847000": {
        "Centro Poblado": "URRAO"
    },
    "05847003": {
        "Centro Poblado": "LA ENCARNACIÓN"
    },
    "05847017": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "05854000": {
        "Centro Poblado": "VALDIVIA"
    },
    "05854002": {
        "Centro Poblado": "PUERTO VALDIVIA"
    },
    "05854003": {
        "Centro Poblado": "RAUDAL VIEJO"
    },
    "05854010": {
        "Centro Poblado": "PUERTO RAUDAL"
    },
    "05856000": {
        "Centro Poblado": "VALPARAÍSO"
    },
    "05858000": {
        "Centro Poblado": "VEGACHÍ"
    },
    "05858001": {
        "Centro Poblado": "EL TIGRE"
    },
    "05858003": {
        "Centro Poblado": "EL CINCO"
    },
    "05861000": {
        "Centro Poblado": "VENECIA"
    },
    "05861002": {
        "Centro Poblado": "BOLOMBOLO"
    },
    "05861006": {
        "Centro Poblado": "PALENQUE"
    },
    "05861008": {
        "Centro Poblado": "LA AMALIA"
    },
    "05873000": {
        "Centro Poblado": "VIGÍA DEL FUERTE"
    },
    "05873001": {
        "Centro Poblado": "SAN ANTONIO DE PADUA"
    },
    "05873002": {
        "Centro Poblado": "VEGAEZ"
    },
    "05873004": {
        "Centro Poblado": "SAN ALEJANDRO"
    },
    "05873005": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "05873006": {
        "Centro Poblado": "PUERTO ANTIOQUIA"
    },
    "05873007": {
        "Centro Poblado": "BUCHADO"
    },
    "05873009": {
        "Centro Poblado": "PALO BLANCO"
    },
    "05873010": {
        "Centro Poblado": "BAJO MURRÍ"
    },
    "05873011": {
        "Centro Poblado": "EL ARENAL"
    },
    "05873012": {
        "Centro Poblado": "GUADUALITO"
    },
    "05873013": {
        "Centro Poblado": "LOMA MURRY"
    },
    "05873014": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "05873015": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "05885000": {
        "Centro Poblado": "YALÍ"
    },
    "05885027": {
        "Centro Poblado": "VILLA ANITA"
    },
    "05887000": {
        "Centro Poblado": "YARUMAL"
    },
    "05887003": {
        "Centro Poblado": "CEDEÑO"
    },
    "05887004": {
        "Centro Poblado": "EL CEDRO"
    },
    "05887006": {
        "Centro Poblado": "OCHALÍ"
    },
    "05887007": {
        "Centro Poblado": "LLANOS DE CUIVA"
    },
    "05887009": {
        "Centro Poblado": "EL PUEBLITO"
    },
    "05887021": {
        "Centro Poblado": "LA LOMA"
    },
    "05887022": {
        "Centro Poblado": "MINA VIEJA"
    },
    "05890000": {
        "Centro Poblado": "YOLOMBÓ"
    },
    "05890001": {
        "Centro Poblado": "LA FLORESTA"
    },
    "05890004": {
        "Centro Poblado": "EL RUBÍ"
    },
    "05890009": {
        "Centro Poblado": "VILLANUEVA"
    },
    "05893000": {
        "Centro Poblado": "YONDÓ"
    },
    "05893001": {
        "Centro Poblado": "CIÉNAGA DE BARBACOA - LA PUNTA"
    },
    "05893002": {
        "Centro Poblado": "SAN LUIS BELTRÁN"
    },
    "05893003": {
        "Centro Poblado": "SAN MIGUEL DEL TIGRE"
    },
    "05893005": {
        "Centro Poblado": "BOCAS DE SAN FRANCISCO"
    },
    "05893008": {
        "Centro Poblado": "EL BAGRE"
    },
    "05893009": {
        "Centro Poblado": "BOCAS DE BARBACOAS"
    },
    "05893014": {
        "Centro Poblado": "PUERTO LOS MANGOS"
    },
    "05893015": {
        "Centro Poblado": "PUERTO MATILDE"
    },
    "05893017": {
        "Centro Poblado": "PUERTO TOMAS"
    },
    "05893018": {
        "Centro Poblado": "PUERTO CASABE"
    },
    "05893019": {
        "Centro Poblado": "LA CONDOR"
    },
    "05893021": {
        "Centro Poblado": "CHORRO DE LÁGRIMAS"
    },
    "05895000": {
        "Centro Poblado": "ZARAGOZA"
    },
    "05895003": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "05895004": {
        "Centro Poblado": "PATO"
    },
    "05895008": {
        "Centro Poblado": "VEGAS DE SEGOVIA"
    },
    "05895009": {
        "Centro Poblado": "EL CENIZO"
    },
    "05895010": {
        "Centro Poblado": "EL CRISTO"
    },
    "05895011": {
        "Centro Poblado": "LA CALIENTE"
    },
    "08001000": {
        "Centro Poblado": "BARRANQUILLA, DISTRITO ESPECIAL, INDUSTRIAL Y PORTUARIO"
    },
    "08078000": {
        "Centro Poblado": "BARANOA"
    },
    "08078001": {
        "Centro Poblado": "CAMPECHE"
    },
    "08078002": {
        "Centro Poblado": "PITAL"
    },
    "08078003": {
        "Centro Poblado": "SIBARCO"
    },
    "08137000": {
        "Centro Poblado": "CAMPO DE LA CRUZ"
    },
    "08137001": {
        "Centro Poblado": "BOHÓRQUEZ"
    },
    "08141000": {
        "Centro Poblado": "CANDELARIA"
    },
    "08141001": {
        "Centro Poblado": "SAN JOSÉ DEL CARRETAL"
    },
    "08141002": {
        "Centro Poblado": "BUENAVENTURA DE LEÑA"
    },
    "08296000": {
        "Centro Poblado": "GALAPA"
    },
    "08296001": {
        "Centro Poblado": "PALUATO"
    },
    "08372000": {
        "Centro Poblado": "JUAN DE ACOSTA"
    },
    "08372001": {
        "Centro Poblado": "BOCATOCINO"
    },
    "08372002": {
        "Centro Poblado": "CHORRERA"
    },
    "08372003": {
        "Centro Poblado": "SAN JOSÉ DE SACO"
    },
    "08372004": {
        "Centro Poblado": "SANTA VERÓNICA"
    },
    "08372007": {
        "Centro Poblado": "URBANIZACIÓN PUNTA CANGREJO"
    },
    "08421000": {
        "Centro Poblado": "LURUACO"
    },
    "08421001": {
        "Centro Poblado": "ARROYO DE PIEDRA"
    },
    "08421002": {
        "Centro Poblado": "PALMAR DE CANDELARIA"
    },
    "08421003": {
        "Centro Poblado": "LOS PENDALES"
    },
    "08421004": {
        "Centro Poblado": "SAN JUAN DE TOCAGUA"
    },
    "08421005": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "08421006": {
        "Centro Poblado": "LOS LÍMITES"
    },
    "08421007": {
        "Centro Poblado": "LA PUNTICA"
    },
    "08421012": {
        "Centro Poblado": "BARRIGÓN"
    },
    "08421013": {
        "Centro Poblado": "SOCAVÓN"
    },
    "08433000": {
        "Centro Poblado": "MALAMBO"
    },
    "08433001": {
        "Centro Poblado": "CARACOLÍ"
    },
    "08433004": {
        "Centro Poblado": "LA AGUADA"
    },
    "08433005": {
        "Centro Poblado": "PITALITO"
    },
    "08436000": {
        "Centro Poblado": "MANATÍ"
    },
    "08436001": {
        "Centro Poblado": "EL PORVENIR (LAS COMPUERTAS)"
    },
    "08436002": {
        "Centro Poblado": "VILLA JUANA"
    },
    "08520000": {
        "Centro Poblado": "PALMAR DE VARELA"
    },
    "08520001": {
        "Centro Poblado": "BURRUSCOS"
    },
    "08549000": {
        "Centro Poblado": "PIOJÓ"
    },
    "08549001": {
        "Centro Poblado": "AGUAS VIVAS"
    },
    "08549002": {
        "Centro Poblado": "EL CERRITO"
    },
    "08549003": {
        "Centro Poblado": "HIBACHARO"
    },
    "08558000": {
        "Centro Poblado": "POLONUEVO"
    },
    "08558001": {
        "Centro Poblado": "PITAL DEL CARLÍN (PITALITO)"
    },
    "08560000": {
        "Centro Poblado": "PONEDERA"
    },
    "08560001": {
        "Centro Poblado": "LA RETIRADA"
    },
    "08560002": {
        "Centro Poblado": "MARTILLO"
    },
    "08560003": {
        "Centro Poblado": "PUERTO GIRALDO"
    },
    "08560004": {
        "Centro Poblado": "SANTA RITA"
    },
    "08573000": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "08573002": {
        "Centro Poblado": "SALGAR"
    },
    "08573003": {
        "Centro Poblado": "SABANILLA (MONTE CARMELO)"
    },
    "08606000": {
        "Centro Poblado": "REPELÓN"
    },
    "08606001": {
        "Centro Poblado": "ARROYO NEGRO"
    },
    "08606002": {
        "Centro Poblado": "CIEN PESOS"
    },
    "08606003": {
        "Centro Poblado": "LAS TABLAS"
    },
    "08606004": {
        "Centro Poblado": "ROTINET"
    },
    "08606005": {
        "Centro Poblado": "VILLA ROSA"
    },
    "08606009": {
        "Centro Poblado": "PITA"
    },
    "08634000": {
        "Centro Poblado": "SABANAGRANDE"
    },
    "08638000": {
        "Centro Poblado": "SABANALARGA"
    },
    "08638001": {
        "Centro Poblado": "AGUADA DE PABLO"
    },
    "08638002": {
        "Centro Poblado": "CASCAJAL"
    },
    "08638003": {
        "Centro Poblado": "COLOMBIA"
    },
    "08638004": {
        "Centro Poblado": "ISABEL LÓPEZ"
    },
    "08638005": {
        "Centro Poblado": "LA PEÑA"
    },
    "08638006": {
        "Centro Poblado": "MOLINERO"
    },
    "08638007": {
        "Centro Poblado": "MIRADOR"
    },
    "08638008": {
        "Centro Poblado": "GALLEGO"
    },
    "08638010": {
        "Centro Poblado": "PATILLA"
    },
    "08675000": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "08675001": {
        "Centro Poblado": "ALGODONAL"
    },
    "08685000": {
        "Centro Poblado": "SANTO TOMÁS"
    },
    "08758000": {
        "Centro Poblado": "SOLEDAD"
    },
    "08770000": {
        "Centro Poblado": "SUAN"
    },
    "08832000": {
        "Centro Poblado": "TUBARÁ"
    },
    "08832001": {
        "Centro Poblado": "CUATRO BOCAS"
    },
    "08832002": {
        "Centro Poblado": "EL MORRO"
    },
    "08832003": {
        "Centro Poblado": "GUAIMARAL"
    },
    "08832004": {
        "Centro Poblado": "JUARUCO"
    },
    "08832007": {
        "Centro Poblado": "CORRAL DE SAN LUIS"
    },
    "08832010": {
        "Centro Poblado": "PLAYA MENDOZA"
    },
    "08832011": {
        "Centro Poblado": "PLAYAS DE EDRIMÁN"
    },
    "08832012": {
        "Centro Poblado": "VILLAS DE PALMARITO"
    },
    "08832013": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "08849000": {
        "Centro Poblado": "USIACURÍ"
    },
    "11001000": {
        "Centro Poblado": "BOGOTÁ, D.C.,BOGOTÁ, DISTRITO CAPITAL"
    },
    "11001002": {
        "Centro Poblado": "BOGOTÁ, D.C.,NAZARETH"
    },
    "11001007": {
        "Centro Poblado": "BOGOTÁ, D.C.,PASQUILLA"
    },
    "11001008": {
        "Centro Poblado": "BOGOTÁ, D.C.,SAN JUAN"
    },
    "11001009": {
        "Centro Poblado": "BOGOTÁ, D.C.,BETANIA"
    },
    "11001010": {
        "Centro Poblado": "BOGOTÁ, D.C.,LA UNIÓN"
    },
    "11001011": {
        "Centro Poblado": "BOGOTÁ, D.C.,MOCHUELO ALTO"
    },
    "11001012": {
        "Centro Poblado": "BOGOTÁ, D.C.,CHORRILLOS"
    },
    "11001013": {
        "Centro Poblado": "BOGOTÁ, D.C.,EL DESTINO"
    },
    "11001014": {
        "Centro Poblado": "BOGOTÁ, D.C.,NUEVA GRANADA"
    },
    "11001015": {
        "Centro Poblado": "BOGOTÁ, D.C.,QUIBA BAJO"
    },
    "13001000": {
        "Centro Poblado": "CARTAGENA DE INDIAS, DISTRITO TURÍSTICO Y CULTURAL"
    },
    "13001001": {
        "Centro Poblado": "ARROYO DE PIEDRA"
    },
    "13001002": {
        "Centro Poblado": "ARROYO GRANDE"
    },
    "13001003": {
        "Centro Poblado": "BARÚ"
    },
    "13001004": {
        "Centro Poblado": "BAYUNCA"
    },
    "13001005": {
        "Centro Poblado": "BOCACHICA"
    },
    "13001006": {
        "Centro Poblado": "CAÑO DEL ORO"
    },
    "13001007": {
        "Centro Poblado": "ISLA FUERTE"
    },
    "13001008": {
        "Centro Poblado": "LA BOQUILLA"
    },
    "13001009": {
        "Centro Poblado": "PASACABALLOS"
    },
    "13001010": {
        "Centro Poblado": "PUNTA CANOA"
    },
    "13001012": {
        "Centro Poblado": "SANTA ANA"
    },
    "13001013": {
        "Centro Poblado": "TIERRA BOMBA"
    },
    "13001014": {
        "Centro Poblado": "PUNTA ARENA"
    },
    "13001015": {
        "Centro Poblado": "ARARCA"
    },
    "13001016": {
        "Centro Poblado": "LETICIA"
    },
    "13001017": {
        "Centro Poblado": "SANTA CRUZ DEL ISLOTE (ARCHIPIÉLAGO DE SAN BERNARDO)"
    },
    "13001018": {
        "Centro Poblado": "EL RECREO"
    },
    "13001019": {
        "Centro Poblado": "PUERTO REY"
    },
    "13001020": {
        "Centro Poblado": "PONTEZUELA"
    },
    "13001026": {
        "Centro Poblado": "ARROYO DE LAS CANOAS"
    },
    "13001027": {
        "Centro Poblado": "EL PUEBLITO"
    },
    "13001028": {
        "Centro Poblado": "LAS EUROPAS"
    },
    "13001029": {
        "Centro Poblado": "MANZANILLO DEL MAR"
    },
    "13001030": {
        "Centro Poblado": "TIERRA BAJA"
    },
    "13001033": {
        "Centro Poblado": "MEMBRILLAL"
    },
    "13001034": {
        "Centro Poblado": "BARCELONA DE INDIAS"
    },
    "13001035": {
        "Centro Poblado": "CARTAGENA LAGUNA CLUB"
    },
    "13001036": {
        "Centro Poblado": "CASAS DEL MAR"
    },
    "13001037": {
        "Centro Poblado": "MÚCURA"
    },
    "13001038": {
        "Centro Poblado": "PUERTO BELLO"
    },
    "13006000": {
        "Centro Poblado": "ACHÍ"
    },
    "13006002": {
        "Centro Poblado": "BOYACÁ"
    },
    "13006003": {
        "Centro Poblado": "BUENAVISTA"
    },
    "13006005": {
        "Centro Poblado": "ALGARROBO"
    },
    "13006007": {
        "Centro Poblado": "GUACAMAYO"
    },
    "13006011": {
        "Centro Poblado": "PLAYA ALTA"
    },
    "13006015": {
        "Centro Poblado": "TACUYA ALTA"
    },
    "13006017": {
        "Centro Poblado": "TRES CRUCES"
    },
    "13006019": {
        "Centro Poblado": "PAYANDÉ"
    },
    "13006020": {
        "Centro Poblado": "RÍO NUEVO"
    },
    "13006021": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "13006022": {
        "Centro Poblado": "PUERTO ISABEL"
    },
    "13006030": {
        "Centro Poblado": "CENTRO ALEGRE"
    },
    "13006033": {
        "Centro Poblado": "PUERTO VENECIA"
    },
    "13006035": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13006039": {
        "Centro Poblado": "LOS NÍSPEROS"
    },
    "13006041": {
        "Centro Poblado": "PARAÍSO SINCERÍN"
    },
    "13006042": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "13030000": {
        "Centro Poblado": "ALTOS DEL ROSARIO"
    },
    "13030001": {
        "Centro Poblado": "EL RUBIO"
    },
    "13030002": {
        "Centro Poblado": "LA PACHA"
    },
    "13030003": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "13030004": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13030005": {
        "Centro Poblado": "SAN ISIDRO 2"
    },
    "13042000": {
        "Centro Poblado": "ARENAL"
    },
    "13042001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "13042002": {
        "Centro Poblado": "CARNIZALA"
    },
    "13042003": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "13042007": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "13052000": {
        "Centro Poblado": "ARJONA"
    },
    "13052001": {
        "Centro Poblado": "PUERTO BADEL (CAÑO SALADO)"
    },
    "13052002": {
        "Centro Poblado": "GAMBOTE"
    },
    "13052003": {
        "Centro Poblado": "ROCHA"
    },
    "13052004": {
        "Centro Poblado": "SINCERÍN"
    },
    "13052005": {
        "Centro Poblado": "SAN RAFAEL DE LA CRUZ"
    },
    "13052008": {
        "Centro Poblado": "EL REMANSO"
    },
    "13062000": {
        "Centro Poblado": "ARROYOHONDO"
    },
    "13062001": {
        "Centro Poblado": "MACHADO"
    },
    "13062002": {
        "Centro Poblado": "MONROY"
    },
    "13062003": {
        "Centro Poblado": "PILÓN"
    },
    "13062004": {
        "Centro Poblado": "SATO"
    },
    "13062006": {
        "Centro Poblado": "SAN FRANCISCO (SOLABANDA)"
    },
    "13074000": {
        "Centro Poblado": "BARRANCO DE LOBA"
    },
    "13074003": {
        "Centro Poblado": "RÍONUEVO"
    },
    "13074004": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "13074005": {
        "Centro Poblado": "LOS CERRITOS"
    },
    "13074006": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "13140000": {
        "Centro Poblado": "CALAMAR"
    },
    "13140002": {
        "Centro Poblado": "BARRANCA NUEVA"
    },
    "13140003": {
        "Centro Poblado": "BARRANCA VIEJA"
    },
    "13140004": {
        "Centro Poblado": "HATO VIEJO"
    },
    "13140009": {
        "Centro Poblado": "YUCAL"
    },
    "13140011": {
        "Centro Poblado": "EL PROGRESO"
    },
    "13160000": {
        "Centro Poblado": "CANTAGALLO"
    },
    "13160001": {
        "Centro Poblado": "SAN LORENZO"
    },
    "13160002": {
        "Centro Poblado": "BRISAS DE BOLÍVAR"
    },
    "13160011": {
        "Centro Poblado": "LA VICTORIA"
    },
    "13160015": {
        "Centro Poblado": "LOS PATICOS"
    },
    "13160017": {
        "Centro Poblado": "NO HAY COMO DIOS"
    },
    "13160019": {
        "Centro Poblado": "SINZONA"
    },
    "13160021": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "13160022": {
        "Centro Poblado": "LA PEÑA"
    },
    "13160023": {
        "Centro Poblado": "PATICO BAJO"
    },
    "13160024": {
        "Centro Poblado": "CUATRO BOCAS"
    },
    "13188000": {
        "Centro Poblado": "CICUCO"
    },
    "13188001": {
        "Centro Poblado": "CAMPO SERENO"
    },
    "13188002": {
        "Centro Poblado": "LA PEÑA"
    },
    "13188003": {
        "Centro Poblado": "SAN FRANCISCO DE LOBA"
    },
    "13188005": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13188006": {
        "Centro Poblado": "BODEGA"
    },
    "13212000": {
        "Centro Poblado": "CÓRDOBA"
    },
    "13212001": {
        "Centro Poblado": "GUAIMARAL"
    },
    "13212003": {
        "Centro Poblado": "LA MONTAÑA DE ALONSO (MARTÍN ALONSO)"
    },
    "13212005": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "13212006": {
        "Centro Poblado": "SINCELEJITO"
    },
    "13212007": {
        "Centro Poblado": "TACAMOCHITO"
    },
    "13212008": {
        "Centro Poblado": "TACAMOCHO"
    },
    "13212009": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13212010": {
        "Centro Poblado": "LA SIERRA"
    },
    "13212011": {
        "Centro Poblado": "LAS MARÍAS"
    },
    "13212012": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13212013": {
        "Centro Poblado": "SANAHUARE"
    },
    "13212014": {
        "Centro Poblado": "SOCORRO 1"
    },
    "13212015": {
        "Centro Poblado": "BELLAVISTA"
    },
    "13212016": {
        "Centro Poblado": "LAS LOMITAS"
    },
    "13212017": {
        "Centro Poblado": "CALIFORNIA"
    },
    "13222000": {
        "Centro Poblado": "CLEMENCIA"
    },
    "13222001": {
        "Centro Poblado": "LAS CARAS"
    },
    "13222002": {
        "Centro Poblado": "EL PEÑIQUE"
    },
    "13244000": {
        "Centro Poblado": "EL CARMEN DE BOLÍVAR"
    },
    "13244001": {
        "Centro Poblado": "BAJO GRANDE"
    },
    "13244002": {
        "Centro Poblado": "CARACOLÍ GRANDE"
    },
    "13244003": {
        "Centro Poblado": "EL SALADO"
    },
    "13244004": {
        "Centro Poblado": "JESÚS DEL MONTE"
    },
    "13244005": {
        "Centro Poblado": "MACAYEPOS"
    },
    "13244006": {
        "Centro Poblado": "SAN CARLOS"
    },
    "13244007": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "13244008": {
        "Centro Poblado": "HATO NUEVO"
    },
    "13244011": {
        "Centro Poblado": "EL RAIZAL"
    },
    "13244014": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13244017": {
        "Centro Poblado": "SANTO DOMINGO DE MEZA"
    },
    "13244018": {
        "Centro Poblado": "EL HOBO"
    },
    "13244019": {
        "Centro Poblado": "ARROYO ARENA"
    },
    "13244020": {
        "Centro Poblado": "LÁZARO"
    },
    "13244021": {
        "Centro Poblado": "PADULA"
    },
    "13244022": {
        "Centro Poblado": "VERDÚN"
    },
    "13248000": {
        "Centro Poblado": "EL GUAMO"
    },
    "13248001": {
        "Centro Poblado": "LA ENEA"
    },
    "13248002": {
        "Centro Poblado": "SAN JOSÉ DE LATA"
    },
    "13248003": {
        "Centro Poblado": "NERVITÍ"
    },
    "13248004": {
        "Centro Poblado": "ROBLES"
    },
    "13248005": {
        "Centro Poblado": "TASAJERA"
    },
    "13268000": {
        "Centro Poblado": "EL PEÑÓN"
    },
    "13268003": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "13268004": {
        "Centro Poblado": "CASTAÑAL"
    },
    "13268006": {
        "Centro Poblado": "LA CHAPETONA"
    },
    "13268008": {
        "Centro Poblado": "JAPÓN"
    },
    "13268013": {
        "Centro Poblado": "LA HUMAREDA"
    },
    "13268017": {
        "Centro Poblado": "PEÑONCITO"
    },
    "13300000": {
        "Centro Poblado": "HATILLO DE LOBA"
    },
    "13300001": {
        "Centro Poblado": "EL POZÓN"
    },
    "13300002": {
        "Centro Poblado": "JUANA SÁNCHEZ"
    },
    "13300003": {
        "Centro Poblado": "LA RIBONA"
    },
    "13300004": {
        "Centro Poblado": "LA VICTORIA"
    },
    "13300005": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13300006": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "13300007": {
        "Centro Poblado": "CERRO DE LAS AGUADAS"
    },
    "13300008": {
        "Centro Poblado": "LAS BRISAS"
    },
    "13300009": {
        "Centro Poblado": "GUALÍ"
    },
    "13300010": {
        "Centro Poblado": "LAS PALMAS"
    },
    "13430000": {
        "Centro Poblado": "MAGANGUÉ"
    },
    "13430001": {
        "Centro Poblado": "BARBOSA"
    },
    "13430002": {
        "Centro Poblado": "BARRANCA DE YUCA"
    },
    "13430003": {
        "Centro Poblado": "BETANIA"
    },
    "13430004": {
        "Centro Poblado": "BOCA DE SAN ANTONIO"
    },
    "13430006": {
        "Centro Poblado": "CASCAJAL"
    },
    "13430007": {
        "Centro Poblado": "CEIBAL"
    },
    "13430008": {
        "Centro Poblado": "COYONGAL"
    },
    "13430009": {
        "Centro Poblado": "EL RETIRO"
    },
    "13430010": {
        "Centro Poblado": "GUAZO"
    },
    "13430011": {
        "Centro Poblado": "HENEQUÉN"
    },
    "13430013": {
        "Centro Poblado": "JUAN ARIAS"
    },
    "13430014": {
        "Centro Poblado": "LA PASCUALA"
    },
    "13430015": {
        "Centro Poblado": "LA VENTURA"
    },
    "13430016": {
        "Centro Poblado": "LAS BRISAS"
    },
    "13430017": {
        "Centro Poblado": "MADRID"
    },
    "13430018": {
        "Centro Poblado": "PALMARITO"
    },
    "13430019": {
        "Centro Poblado": "PANSEGÜITA"
    },
    "13430020": {
        "Centro Poblado": "PIÑALITO"
    },
    "13430021": {
        "Centro Poblado": "SAN RAFAEL DE CORTINA"
    },
    "13430022": {
        "Centro Poblado": "SAN JOSÉ DE LAS MARTAS"
    },
    "13430023": {
        "Centro Poblado": "SAN SEBASTIÁN DE BUENAVISTA"
    },
    "13430024": {
        "Centro Poblado": "SANTA FE"
    },
    "13430025": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13430026": {
        "Centro Poblado": "SANTA MÓNICA"
    },
    "13430027": {
        "Centro Poblado": "SANTA PABLA"
    },
    "13430028": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "13430029": {
        "Centro Poblado": "PUERTO KENNEDY"
    },
    "13430030": {
        "Centro Poblado": "TACALOA"
    },
    "13430031": {
        "Centro Poblado": "TACASALUMA"
    },
    "13430032": {
        "Centro Poblado": "TOLÚ"
    },
    "13430036": {
        "Centro Poblado": "PLAYA DE LAS FLORES"
    },
    "13430038": {
        "Centro Poblado": "EL CUATRO"
    },
    "13430039": {
        "Centro Poblado": "BOCA DE GUAMAL"
    },
    "13430040": {
        "Centro Poblado": "TRES PUNTAS"
    },
    "13430041": {
        "Centro Poblado": "EMAUS"
    },
    "13430047": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "13430048": {
        "Centro Poblado": "PUNTA DE CARTAGENA"
    },
    "13430049": {
        "Centro Poblado": "ROMA"
    },
    "13430051": {
        "Centro Poblado": "SAN ANTOÑITO"
    },
    "13430052": {
        "Centro Poblado": "SANTA COITA"
    },
    "13430053": {
        "Centro Poblado": "FLORENCIA"
    },
    "13433000": {
        "Centro Poblado": "MAHATES"
    },
    "13433001": {
        "Centro Poblado": "EVITAR"
    },
    "13433002": {
        "Centro Poblado": "GAMERO"
    },
    "13433003": {
        "Centro Poblado": "MALAGANA"
    },
    "13433004": {
        "Centro Poblado": "SAN BASILIO DE PALENQUE"
    },
    "13433005": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "13433009": {
        "Centro Poblado": "MANDINGA"
    },
    "13433010": {
        "Centro Poblado": "CRUZ DEL VIZO"
    },
    "13433011": {
        "Centro Poblado": "LA MANGA"
    },
    "13440000": {
        "Centro Poblado": "MARGARITA"
    },
    "13440001": {
        "Centro Poblado": "BOTÓN DE LEIVA"
    },
    "13440002": {
        "Centro Poblado": "CANTERA"
    },
    "13440003": {
        "Centro Poblado": "CAUSADO"
    },
    "13440004": {
        "Centro Poblado": "CHILLOA"
    },
    "13440005": {
        "Centro Poblado": "DOÑA JUANA"
    },
    "13440007": {
        "Centro Poblado": "MAMONCITO"
    },
    "13440008": {
        "Centro Poblado": "SANDOVAL"
    },
    "13440010": {
        "Centro Poblado": "SAN JOSÉ DE LOS TRAPICHES"
    },
    "13440011": {
        "Centro Poblado": "COROCITO"
    },
    "13440012": {
        "Centro Poblado": "GUATAQUITA"
    },
    "13440014": {
        "Centro Poblado": "CAÑO MONO"
    },
    "13440017": {
        "Centro Poblado": "LA MONTAÑA"
    },
    "13442000": {
        "Centro Poblado": "MARÍA LA BAJA"
    },
    "13442001": {
        "Centro Poblado": "CORREA"
    },
    "13442002": {
        "Centro Poblado": "EL NÍSPERO"
    },
    "13442003": {
        "Centro Poblado": "FLAMENCO"
    },
    "13442004": {
        "Centro Poblado": "MANPUJÁN"
    },
    "13442005": {
        "Centro Poblado": "ÑANGUMA"
    },
    "13442006": {
        "Centro Poblado": "RETIRO NUEVO"
    },
    "13442007": {
        "Centro Poblado": "SAN JOSÉ DEL PLAYÓN"
    },
    "13442008": {
        "Centro Poblado": "SAN PABLO"
    },
    "13442009": {
        "Centro Poblado": "EL MAJAGUA"
    },
    "13442011": {
        "Centro Poblado": "LOS BELLOS"
    },
    "13442012": {
        "Centro Poblado": "MATUYA"
    },
    "13442014": {
        "Centro Poblado": "COLÚ"
    },
    "13442015": {
        "Centro Poblado": "EL FLORIDO"
    },
    "13442016": {
        "Centro Poblado": "NUEVO RETÉN"
    },
    "13442017": {
        "Centro Poblado": "ARROYO GRANDE"
    },
    "13442019": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "13442020": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13442022": {
        "Centro Poblado": "PRIMERO DE JULIO"
    },
    "13442023": {
        "Centro Poblado": "EL SENA"
    },
    "13442024": {
        "Centro Poblado": "LA CURVA"
    },
    "13442025": {
        "Centro Poblado": "LA PISTA"
    },
    "13442026": {
        "Centro Poblado": "MARQUEZ"
    },
    "13442027": {
        "Centro Poblado": "MUNGUIA"
    },
    "13442030": {
        "Centro Poblado": "CEDRITO"
    },
    "13442031": {
        "Centro Poblado": "EL GUAMO"
    },
    "13442034": {
        "Centro Poblado": "GUARISMO"
    },
    "13442035": {
        "Centro Poblado": "LA SUPREMA"
    },
    "13442040": {
        "Centro Poblado": "NUEVO PORVENIR"
    },
    "13442043": {
        "Centro Poblado": "SUCESIÓN"
    },
    "13442044": {
        "Centro Poblado": "TOMA RAZÓN"
    },
    "13442045": {
        "Centro Poblado": "EL PUEBLITO"
    },
    "13458000": {
        "Centro Poblado": "MONTECRISTO"
    },
    "13458001": {
        "Centro Poblado": "BETANIA"
    },
    "13458002": {
        "Centro Poblado": "LA DORADA"
    },
    "13458003": {
        "Centro Poblado": "PARAÍSO"
    },
    "13458004": {
        "Centro Poblado": "PUEBLO LINDO"
    },
    "13458005": {
        "Centro Poblado": "PUEBLO NUEVO - REGENCIA"
    },
    "13458006": {
        "Centro Poblado": "PUERTO ESPAÑA"
    },
    "13458007": {
        "Centro Poblado": "PLATANAL"
    },
    "13458008": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "13458012": {
        "Centro Poblado": "VILLA URIBE"
    },
    "13468000": {
        "Centro Poblado": "SANTA CRUZ DE MOMPOX, DISTRITO ESPECIAL, TURÍSTICO, CULTURAL E HISTÓRICO"
    },
    "13468001": {
        "Centro Poblado": "CALDERA"
    },
    "13468002": {
        "Centro Poblado": "CANDELARIA"
    },
    "13468008": {
        "Centro Poblado": "GUAIMARAL"
    },
    "13468009": {
        "Centro Poblado": "GUATACA"
    },
    "13468010": {
        "Centro Poblado": "LA JAGUA"
    },
    "13468011": {
        "Centro Poblado": "LA LOBATA"
    },
    "13468013": {
        "Centro Poblado": "LA RINCONADA"
    },
    "13468014": {
        "Centro Poblado": "LAS BOQUILLAS"
    },
    "13468015": {
        "Centro Poblado": "LOMA DE SIMÓN"
    },
    "13468016": {
        "Centro Poblado": "LOS PIÑONES"
    },
    "13468020": {
        "Centro Poblado": "SAN IGNACIO"
    },
    "13468022": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "13468023": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "13468024": {
        "Centro Poblado": "SANTA ROSA"
    },
    "13468025": {
        "Centro Poblado": "SANTA TERESITA"
    },
    "13468028": {
        "Centro Poblado": "ANCÓN"
    },
    "13468030": {
        "Centro Poblado": "LA TRAVESÍA"
    },
    "13468031": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13468033": {
        "Centro Poblado": "BOMBA"
    },
    "13468036": {
        "Centro Poblado": "EL ROSARIO"
    },
    "13468038": {
        "Centro Poblado": "SANTA ELENA"
    },
    "13468039": {
        "Centro Poblado": "SAN LUIS"
    },
    "13468040": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "13473000": {
        "Centro Poblado": "MORALES"
    },
    "13473002": {
        "Centro Poblado": "BODEGA CENTRAL"
    },
    "13473003": {
        "Centro Poblado": "EL DIQUE"
    },
    "13473004": {
        "Centro Poblado": "LAS PAILAS"
    },
    "13473012": {
        "Centro Poblado": "BOCA DE LA HONDA"
    },
    "13473013": {
        "Centro Poblado": "MICOAHUMADO"
    },
    "13473014": {
        "Centro Poblado": "PAREDES DE ORORIA"
    },
    "13473015": {
        "Centro Poblado": "EL CORCOVADO"
    },
    "13473016": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "13473017": {
        "Centro Poblado": "LA PALMA"
    },
    "13473019": {
        "Centro Poblado": "BOCA DE LA CIENAGA"
    },
    "13490000": {
        "Centro Poblado": "NOROSÍ"
    },
    "13490001": {
        "Centro Poblado": "BUENA SEÑA"
    },
    "13490002": {
        "Centro Poblado": "CASA DE BARRO"
    },
    "13490003": {
        "Centro Poblado": "LAS NIEVES"
    },
    "13490004": {
        "Centro Poblado": "MINA BRISA"
    },
    "13490005": {
        "Centro Poblado": "MINA ESTRELLA"
    },
    "13490006": {
        "Centro Poblado": "OLIVARES"
    },
    "13490007": {
        "Centro Poblado": "SANTA ELENA"
    },
    "13490008": {
        "Centro Poblado": "VILLA ARIZA"
    },
    "13549000": {
        "Centro Poblado": "PINILLOS"
    },
    "13549001": {
        "Centro Poblado": "ARMENIA"
    },
    "13549004": {
        "Centro Poblado": "LA RUFINA"
    },
    "13549005": {
        "Centro Poblado": "LA UNION"
    },
    "13549007": {
        "Centro Poblado": "LAS FLORES"
    },
    "13549009": {
        "Centro Poblado": "MANTEQUERA"
    },
    "13549010": {
        "Centro Poblado": "PALENQUITO"
    },
    "13549011": {
        "Centro Poblado": "PALOMINO"
    },
    "13549012": {
        "Centro Poblado": "PUERTO LÓPEZ"
    },
    "13549014": {
        "Centro Poblado": "SANTA COA"
    },
    "13549015": {
        "Centro Poblado": "SANTA ROSA"
    },
    "13549018": {
        "Centro Poblado": "RUFINA NUEVA"
    },
    "13549024": {
        "Centro Poblado": "LA VICTORIA"
    },
    "13549025": {
        "Centro Poblado": "LOS LIMONES"
    },
    "13549032": {
        "Centro Poblado": "TAPOA"
    },
    "13549034": {
        "Centro Poblado": "LA UNION CABECERA"
    },
    "13580000": {
        "Centro Poblado": "REGIDOR"
    },
    "13580001": {
        "Centro Poblado": "PIÑAL"
    },
    "13580003": {
        "Centro Poblado": "LOS CAIMANES"
    },
    "13580004": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "13580005": {
        "Centro Poblado": "SAN CAYETANO"
    },
    "13580006": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "13580007": {
        "Centro Poblado": "SANTA TERESA"
    },
    "13600000": {
        "Centro Poblado": "RÍO VIEJO"
    },
    "13600007": {
        "Centro Poblado": "CAIMITAL"
    },
    "13600009": {
        "Centro Poblado": "COBADILLO"
    },
    "13600010": {
        "Centro Poblado": "HATILLO"
    },
    "13600011": {
        "Centro Poblado": "MACEDONIA"
    },
    "13600014": {
        "Centro Poblado": "SIERPETUERTA"
    },
    "13620000": {
        "Centro Poblado": "SAN CRISTÓBAL"
    },
    "13620001": {
        "Centro Poblado": "HIGUERETAL"
    },
    "13620002": {
        "Centro Poblado": "LAS CRUCES"
    },
    "13647000": {
        "Centro Poblado": "SAN ESTANISLAO DE KOSTKA"
    },
    "13647002": {
        "Centro Poblado": "LAS PIEDRAS"
    },
    "13650000": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "13650001": {
        "Centro Poblado": "GUASIMAL"
    },
    "13650002": {
        "Centro Poblado": "MENCHIQUEJO"
    },
    "13650004": {
        "Centro Poblado": "PUNTA DE HORNOS"
    },
    "13650005": {
        "Centro Poblado": "SANTA ROSA"
    },
    "13650006": {
        "Centro Poblado": "EL PALMAR"
    },
    "13650008": {
        "Centro Poblado": "EL PORVENIR"
    },
    "13650009": {
        "Centro Poblado": "CUATRO BOCAS"
    },
    "13650010": {
        "Centro Poblado": "EL CONTADERO"
    },
    "13650013": {
        "Centro Poblado": "LA GUADUA"
    },
    "13650014": {
        "Centro Poblado": "LAS CUEVAS"
    },
    "13650015": {
        "Centro Poblado": "PAMPANILLO"
    },
    "13654000": {
        "Centro Poblado": "SAN JACINTO"
    },
    "13654001": {
        "Centro Poblado": "ARENAS"
    },
    "13654002": {
        "Centro Poblado": "BAJO GRANDE"
    },
    "13654003": {
        "Centro Poblado": "LAS PALMAS"
    },
    "13654005": {
        "Centro Poblado": "SAN CRISTÓBAL"
    },
    "13654006": {
        "Centro Poblado": "LAS CHARQUITAS"
    },
    "13654007": {
        "Centro Poblado": "PARAÍSO"
    },
    "13654008": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "13655000": {
        "Centro Poblado": "SAN JACINTO DEL CAUCA"
    },
    "13655001": {
        "Centro Poblado": "TENCHE"
    },
    "13655003": {
        "Centro Poblado": "CAIMITAL"
    },
    "13655004": {
        "Centro Poblado": "LA RAYA"
    },
    "13655005": {
        "Centro Poblado": "GALINDO"
    },
    "13655006": {
        "Centro Poblado": "MÉJICO"
    },
    "13655007": {
        "Centro Poblado": "ASTILLEROS"
    },
    "13657000": {
        "Centro Poblado": "SAN JUAN NEPOMUCENO"
    },
    "13657001": {
        "Centro Poblado": "CORRALITO"
    },
    "13657002": {
        "Centro Poblado": "LA HAYA"
    },
    "13657003": {
        "Centro Poblado": "SAN JOSÉ DEL PEÑÓN (LAS PORQUERAS)"
    },
    "13657004": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "13657005": {
        "Centro Poblado": "SAN CAYETANO"
    },
    "13657006": {
        "Centro Poblado": "SAN PEDRO CONSOLADO"
    },
    "13667000": {
        "Centro Poblado": "SAN MARTÍN DE LOBA"
    },
    "13667002": {
        "Centro Poblado": "CHIMI"
    },
    "13667009": {
        "Centro Poblado": "PAPAYAL"
    },
    "13667010": {
        "Centro Poblado": "LAS PLAYITAS"
    },
    "13667014": {
        "Centro Poblado": "PUEBLO NUEVO CERRO DE JULIO"
    },
    "13667015": {
        "Centro Poblado": "EL JOBO"
    },
    "13667016": {
        "Centro Poblado": "EL VARAL"
    },
    "13667017": {
        "Centro Poblado": "LOS PUEBLOS"
    },
    "13670000": {
        "Centro Poblado": "SAN PABLO"
    },
    "13670002": {
        "Centro Poblado": "CANALETAL"
    },
    "13670003": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "13670004": {
        "Centro Poblado": "EL CARMEN"
    },
    "13670005": {
        "Centro Poblado": "EL SOCORRO"
    },
    "13670007": {
        "Centro Poblado": "POZO AZUL"
    },
    "13670009": {
        "Centro Poblado": "CAÑABRAVAL"
    },
    "13670010": {
        "Centro Poblado": "AGUA SUCIA"
    },
    "13670011": {
        "Centro Poblado": "CERRO AZUL"
    },
    "13670012": {
        "Centro Poblado": "VALLECITO"
    },
    "13670013": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "13670014": {
        "Centro Poblado": "LA VIRGENCITA"
    },
    "13670017": {
        "Centro Poblado": "EL ROSARIO"
    },
    "13670018": {
        "Centro Poblado": "LA FRÍA"
    },
    "13670019": {
        "Centro Poblado": "LA UNIÓN"
    },
    "13670020": {
        "Centro Poblado": "LOS CAGUISES"
    },
    "13670022": {
        "Centro Poblado": "LA YE"
    },
    "13673000": {
        "Centro Poblado": "SANTA CATALINA"
    },
    "13673003": {
        "Centro Poblado": "GALERAZAMBA"
    },
    "13673005": {
        "Centro Poblado": "LOMA DE ARENA"
    },
    "13673006": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13673007": {
        "Centro Poblado": "COLORADO"
    },
    "13673009": {
        "Centro Poblado": "EL HOBO"
    },
    "13683000": {
        "Centro Poblado": "SANTA ROSA DE LIMA"
    },
    "13688000": {
        "Centro Poblado": "SANTA ROSA DEL SUR"
    },
    "13688002": {
        "Centro Poblado": "BUENAVISTA"
    },
    "13688005": {
        "Centro Poblado": "FÁTIMA"
    },
    "13688007": {
        "Centro Poblado": "CANELOS"
    },
    "13688009": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "13688011": {
        "Centro Poblado": "SAN LUCAS"
    },
    "13688013": {
        "Centro Poblado": "VILLA FLOR"
    },
    "13688015": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "13688016": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "13688020": {
        "Centro Poblado": "SAN BENITO"
    },
    "13688021": {
        "Centro Poblado": "SANTA LUCIA"
    },
    "13744000": {
        "Centro Poblado": "SIMITÍ"
    },
    "13744001": {
        "Centro Poblado": "CAMPO PALLARES"
    },
    "13744006": {
        "Centro Poblado": "VERACRUZ"
    },
    "13744007": {
        "Centro Poblado": "SAN BLAS"
    },
    "13744008": {
        "Centro Poblado": "SAN LUIS"
    },
    "13744010": {
        "Centro Poblado": "LAS BRISAS"
    },
    "13744011": {
        "Centro Poblado": "MONTERREY"
    },
    "13744013": {
        "Centro Poblado": "ANIMAS ALTAS"
    },
    "13744014": {
        "Centro Poblado": "ANIMAS BAJAS"
    },
    "13744015": {
        "Centro Poblado": "DIAMANTE"
    },
    "13744016": {
        "Centro Poblado": "GARZAL"
    },
    "13744017": {
        "Centro Poblado": "PARAÍSO"
    },
    "13744019": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "13744021": {
        "Centro Poblado": "LAS ACEITUNAS"
    },
    "13744022": {
        "Centro Poblado": "EL PIÑAL"
    },
    "13744023": {
        "Centro Poblado": "LAS PALMERAS"
    },
    "13744024": {
        "Centro Poblado": "PATA PELA"
    },
    "13744025": {
        "Centro Poblado": "SABANA DE SAN LUIS"
    },
    "13760000": {
        "Centro Poblado": "SOPLAVIENTO"
    },
    "13780000": {
        "Centro Poblado": "TALAIGUA NUEVO"
    },
    "13780005": {
        "Centro Poblado": "CAÑOHONDO"
    },
    "13780009": {
        "Centro Poblado": "PORVENIR"
    },
    "13780011": {
        "Centro Poblado": "VESUBIO"
    },
    "13780017": {
        "Centro Poblado": "PATICO"
    },
    "13780023": {
        "Centro Poblado": "TALAIGUA VIEJO"
    },
    "13780024": {
        "Centro Poblado": "LADERA DE SAN MARTÍN"
    },
    "13780025": {
        "Centro Poblado": "PEÑÓN DE DURÁN"
    },
    "13780026": {
        "Centro Poblado": "LOS MANGOS"
    },
    "13780027": {
        "Centro Poblado": "TUPE"
    },
    "13810000": {
        "Centro Poblado": "PUERTO RICO"
    },
    "13810002": {
        "Centro Poblado": "BOCAS DE SOLIS"
    },
    "13810003": {
        "Centro Poblado": "COLORADO"
    },
    "13810004": {
        "Centro Poblado": "DOS BOCAS"
    },
    "13810005": {
        "Centro Poblado": "EL SUDÁN"
    },
    "13810006": {
        "Centro Poblado": "LA VENTURA"
    },
    "13810008": {
        "Centro Poblado": "PUERTO COCA"
    },
    "13810009": {
        "Centro Poblado": "QUEBRADA DEL MEDIO"
    },
    "13810010": {
        "Centro Poblado": "SABANAS DEL FIRME"
    },
    "13810011": {
        "Centro Poblado": "TIQUISIO NUEVO"
    },
    "13810012": {
        "Centro Poblado": "PUERTO GAITAN"
    },
    "13836000": {
        "Centro Poblado": "TURBACO"
    },
    "13836001": {
        "Centro Poblado": "CAÑAVERAL"
    },
    "13836002": {
        "Centro Poblado": "SAN JOSÉ DE CHIQUITO"
    },
    "13836006": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "13836007": {
        "Centro Poblado": "URBANIZACION VILLA DE CALATRAVA"
    },
    "13836008": {
        "Centro Poblado": "URBANIZACION CAMPESTRE"
    },
    "13836009": {
        "Centro Poblado": "URBANIZACION CATALINA"
    },
    "13836010": {
        "Centro Poblado": "URBANIZACION ZAPOTE"
    },
    "13836011": {
        "Centro Poblado": "CONDOMINIO HACIENDA"
    },
    "13838000": {
        "Centro Poblado": "TURBANÁ"
    },
    "13838001": {
        "Centro Poblado": "BALLESTAS"
    },
    "13838002": {
        "Centro Poblado": "LOMAS DE MATUNILLA"
    },
    "13873000": {
        "Centro Poblado": "VILLANUEVA"
    },
    "13873001": {
        "Centro Poblado": "ZIPACOA"
    },
    "13873002": {
        "Centro Poblado": "ALGARROBO"
    },
    "13894000": {
        "Centro Poblado": "ZAMBRANO"
    },
    "13894002": {
        "Centro Poblado": "CAPACA"
    },
    "15001000": {
        "Centro Poblado": "TUNJA"
    },
    "15022000": {
        "Centro Poblado": "ALMEIDA"
    },
    "15047000": {
        "Centro Poblado": "AQUITANIA"
    },
    "15047004": {
        "Centro Poblado": "SAN JUAN DE MOMBITA"
    },
    "15047007": {
        "Centro Poblado": "TOQUILLA"
    },
    "15047010": {
        "Centro Poblado": "DAITÓ"
    },
    "15047012": {
        "Centro Poblado": "PRIMAVERA"
    },
    "15047014": {
        "Centro Poblado": "PÉREZ"
    },
    "15051000": {
        "Centro Poblado": "ARCABUCO"
    },
    "15087000": {
        "Centro Poblado": "BELÉN"
    },
    "15090000": {
        "Centro Poblado": "BERBEO"
    },
    "15092000": {
        "Centro Poblado": "BETÉITIVA"
    },
    "15092001": {
        "Centro Poblado": "OTENGA"
    },
    "15097000": {
        "Centro Poblado": "BOAVITA"
    },
    "15104000": {
        "Centro Poblado": "BOYACÁ"
    },
    "15106000": {
        "Centro Poblado": "BRICEÑO"
    },
    "15109000": {
        "Centro Poblado": "BUENAVISTA"
    },
    "15114000": {
        "Centro Poblado": "BUSBANZÁ"
    },
    "15131000": {
        "Centro Poblado": "CALDAS"
    },
    "15131001": {
        "Centro Poblado": "NARIÑO"
    },
    "15135000": {
        "Centro Poblado": "CAMPOHERMOSO"
    },
    "15135002": {
        "Centro Poblado": "VISTAHERMOSA"
    },
    "15135003": {
        "Centro Poblado": "LOS CEDROS"
    },
    "15162000": {
        "Centro Poblado": "CERINZA"
    },
    "15172000": {
        "Centro Poblado": "CHINAVITA"
    },
    "15176000": {
        "Centro Poblado": "CHIQUINQUIRÁ"
    },
    "15180000": {
        "Centro Poblado": "CHISCAS"
    },
    "15180005": {
        "Centro Poblado": "MERCEDES"
    },
    "15183000": {
        "Centro Poblado": "CHITA"
    },
    "15183002": {
        "Centro Poblado": "EL MORAL"
    },
    "15185000": {
        "Centro Poblado": "CHITARAQUE"
    },
    "15187000": {
        "Centro Poblado": "CHIVATÁ"
    },
    "15189000": {
        "Centro Poblado": "CIÉNEGA"
    },
    "15204000": {
        "Centro Poblado": "CÓMBITA"
    },
    "15204001": {
        "Centro Poblado": "EL BARNE"
    },
    "15204006": {
        "Centro Poblado": "SAN ONOFRE"
    },
    "15212000": {
        "Centro Poblado": "COPER"
    },
    "15215000": {
        "Centro Poblado": "CORRALES"
    },
    "15218000": {
        "Centro Poblado": "COVARACHÍA"
    },
    "15223000": {
        "Centro Poblado": "CUBARÁ"
    },
    "15223005": {
        "Centro Poblado": "EL GUAMO"
    },
    "15223011": {
        "Centro Poblado": "GIBRALTAR"
    },
    "15223012": {
        "Centro Poblado": "PUENTE DE BOJABÁ"
    },
    "15224000": {
        "Centro Poblado": "CUCAITA"
    },
    "15226000": {
        "Centro Poblado": "CUÍTIVA"
    },
    "15226001": {
        "Centro Poblado": "LLANO DE ALARCÓN"
    },
    "15232000": {
        "Centro Poblado": "SAN PEDRO DE IGUAQUE"
    },
    "15232001": {
        "Centro Poblado": "CHÍQUIZA"
    },
    "15236000": {
        "Centro Poblado": "CHIVOR"
    },
    "15238000": {
        "Centro Poblado": "DUITAMA"
    },
    "15238008": {
        "Centro Poblado": "SAN LORENZO ABAJO"
    },
    "15238009": {
        "Centro Poblado": "SAN ANTONIO NORTE"
    },
    "15238011": {
        "Centro Poblado": "LA TRINIDAD"
    },
    "15238012": {
        "Centro Poblado": "CIUDADELA INDUSTRIAL"
    },
    "15238013": {
        "Centro Poblado": "SANTA CLARA"
    },
    "15238014": {
        "Centro Poblado": "TOCOGUA"
    },
    "15238015": {
        "Centro Poblado": "PUEBLITO BOYACENSE"
    },
    "15244000": {
        "Centro Poblado": "EL COCUY"
    },
    "15248000": {
        "Centro Poblado": "EL ESPINO"
    },
    "15272000": {
        "Centro Poblado": "FIRAVITOBA"
    },
    "15276000": {
        "Centro Poblado": "FLORESTA"
    },
    "15276001": {
        "Centro Poblado": "TOBASÍA"
    },
    "15293000": {
        "Centro Poblado": "GACHANTIVÁ"
    },
    "15296000": {
        "Centro Poblado": "GÁMEZA"
    },
    "15299000": {
        "Centro Poblado": "GARAGOA"
    },
    "15317000": {
        "Centro Poblado": "GUACAMAYAS"
    },
    "15322000": {
        "Centro Poblado": "GUATEQUE"
    },
    "15325000": {
        "Centro Poblado": "GUAYATÁ"
    },
    "15332000": {
        "Centro Poblado": "GÜICÁN DE LA SIERRA"
    },
    "15362000": {
        "Centro Poblado": "IZA"
    },
    "15367000": {
        "Centro Poblado": "JENESANO"
    },
    "15368000": {
        "Centro Poblado": "JERICÓ"
    },
    "15368001": {
        "Centro Poblado": "CHEVA"
    },
    "15377000": {
        "Centro Poblado": "LABRANZAGRANDE"
    },
    "15380000": {
        "Centro Poblado": "LA CAPILLA"
    },
    "15401000": {
        "Centro Poblado": "LA VICTORIA"
    },
    "15403000": {
        "Centro Poblado": "LA UVITA"
    },
    "15403001": {
        "Centro Poblado": "CUSAGÜI"
    },
    "15407000": {
        "Centro Poblado": "VILLA DE LEYVA"
    },
    "15407003": {
        "Centro Poblado": "EL ROBLE"
    },
    "15425000": {
        "Centro Poblado": "MACANAL"
    },
    "15425004": {
        "Centro Poblado": "SAN PEDRO DE MUCEÑO"
    },
    "15442000": {
        "Centro Poblado": "MARIPÍ"
    },
    "15442001": {
        "Centro Poblado": "SANTA ROSA"
    },
    "15442002": {
        "Centro Poblado": "ZULIA"
    },
    "15442008": {
        "Centro Poblado": "GUARUMAL"
    },
    "15455000": {
        "Centro Poblado": "MIRAFLORES"
    },
    "15464000": {
        "Centro Poblado": "MONGUA"
    },
    "15466000": {
        "Centro Poblado": "MONGUÍ"
    },
    "15469000": {
        "Centro Poblado": "MONIQUIRÁ"
    },
    "15469007": {
        "Centro Poblado": "LOS CAYENOS"
    },
    "15476000": {
        "Centro Poblado": "MOTAVITA"
    },
    "15480000": {
        "Centro Poblado": "MUZO"
    },
    "15491000": {
        "Centro Poblado": "NOBSA"
    },
    "15491001": {
        "Centro Poblado": "BELENCITO"
    },
    "15491002": {
        "Centro Poblado": "CHAMEZA MAYOR"
    },
    "15491003": {
        "Centro Poblado": "DICHO"
    },
    "15491004": {
        "Centro Poblado": "PUNTA LARGA"
    },
    "15491005": {
        "Centro Poblado": "UCUENGA"
    },
    "15491006": {
        "Centro Poblado": "CALERAS"
    },
    "15491007": {
        "Centro Poblado": "NAZARETH"
    },
    "15491009": {
        "Centro Poblado": "CHÁMEZA MENOR"
    },
    "15491010": {
        "Centro Poblado": "GUAQUIRA"
    },
    "15491012": {
        "Centro Poblado": "SANTANA"
    },
    "15494000": {
        "Centro Poblado": "NUEVO COLÓN"
    },
    "15500000": {
        "Centro Poblado": "OICATÁ"
    },
    "15507000": {
        "Centro Poblado": "OTANCHE"
    },
    "15507001": {
        "Centro Poblado": "BETANIA"
    },
    "15507002": {
        "Centro Poblado": "BUENAVISTA"
    },
    "15507004": {
        "Centro Poblado": "PIZARRA"
    },
    "15507009": {
        "Centro Poblado": "SAN JOSÉ DE NAZARETH"
    },
    "15507010": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "15511000": {
        "Centro Poblado": "PACHAVITA"
    },
    "15514000": {
        "Centro Poblado": "PÁEZ"
    },
    "15514001": {
        "Centro Poblado": "LA URURIA"
    },
    "15514002": {
        "Centro Poblado": "SIRASÍ"
    },
    "15516000": {
        "Centro Poblado": "PAIPA"
    },
    "15516001": {
        "Centro Poblado": "PALERMO"
    },
    "15516005": {
        "Centro Poblado": "PANTANO DE VARGAS"
    },
    "15518000": {
        "Centro Poblado": "PAJARITO"
    },
    "15518001": {
        "Centro Poblado": "CORINTO"
    },
    "15518002": {
        "Centro Poblado": "CURISÍ"
    },
    "15522000": {
        "Centro Poblado": "PANQUEBA"
    },
    "15531000": {
        "Centro Poblado": "PAUNA"
    },
    "15533000": {
        "Centro Poblado": "PAYA"
    },
    "15533001": {
        "Centro Poblado": "MORCOTE"
    },
    "15537000": {
        "Centro Poblado": "PAZ DE RÍO"
    },
    "15537001": {
        "Centro Poblado": "PAZ VIEJA"
    },
    "15542000": {
        "Centro Poblado": "PESCA"
    },
    "15550000": {
        "Centro Poblado": "PISBA"
    },
    "15572000": {
        "Centro Poblado": "PUERTO BOYACÁ"
    },
    "15572001": {
        "Centro Poblado": "GUANEGRO"
    },
    "15572005": {
        "Centro Poblado": "PUERTO GUTIÉRREZ"
    },
    "15572006": {
        "Centro Poblado": "CRUCE PALAGUA"
    },
    "15572007": {
        "Centro Poblado": "PUERTO SERVIEZ"
    },
    "15572008": {
        "Centro Poblado": "EL PESCADO"
    },
    "15572009": {
        "Centro Poblado": "KILÓMETRO DOS Y MEDIO"
    },
    "15572010": {
        "Centro Poblado": "KILÓMETRO 25"
    },
    "15572011": {
        "Centro Poblado": "EL MARFIL"
    },
    "15572012": {
        "Centro Poblado": "PUERTO PINZÓN"
    },
    "15572013": {
        "Centro Poblado": "PUERTO ROMERO"
    },
    "15572017": {
        "Centro Poblado": "CRUCE EL CHAPARRO"
    },
    "15572018": {
        "Centro Poblado": "EL ERMITAÑO"
    },
    "15572019": {
        "Centro Poblado": "EL OKAL"
    },
    "15572020": {
        "Centro Poblado": "EL TRIQUE"
    },
    "15572021": {
        "Centro Poblado": "KILÓMETRO 11"
    },
    "15572023": {
        "Centro Poblado": "MUELLE VELÁSQUEZ"
    },
    "15572024": {
        "Centro Poblado": "PUERTO NIÑO"
    },
    "15572026": {
        "Centro Poblado": "KILÓMETRO UNO Y MEDIO"
    },
    "15572027": {
        "Centro Poblado": "LA CEIBA"
    },
    "15572028": {
        "Centro Poblado": "PALAGUA SEGUNDO SECTOR"
    },
    "15580000": {
        "Centro Poblado": "QUÍPAMA"
    },
    "15580001": {
        "Centro Poblado": "CORMAL"
    },
    "15580002": {
        "Centro Poblado": "EL PARQUE"
    },
    "15580003": {
        "Centro Poblado": "HUMBO"
    },
    "15580005": {
        "Centro Poblado": "EL MANGO (LA YE)"
    },
    "15599000": {
        "Centro Poblado": "RAMIRIQUÍ"
    },
    "15599001": {
        "Centro Poblado": "GUAYABAL (FÁTIMA)"
    },
    "15599004": {
        "Centro Poblado": "EL ESCOBAL"
    },
    "15599005": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "15599006": {
        "Centro Poblado": "VILLA TOSCANA"
    },
    "15600000": {
        "Centro Poblado": "RÁQUIRA"
    },
    "15600002": {
        "Centro Poblado": "LA CANDELARIA"
    },
    "15621000": {
        "Centro Poblado": "RONDÓN"
    },
    "15621001": {
        "Centro Poblado": "RANCHOGRANDE"
    },
    "15632000": {
        "Centro Poblado": "SABOYÁ"
    },
    "15632001": {
        "Centro Poblado": "GARAVITO"
    },
    "15638000": {
        "Centro Poblado": "SÁCHICA"
    },
    "15646000": {
        "Centro Poblado": "SAMACÁ"
    },
    "15646001": {
        "Centro Poblado": "LA CUMBRE"
    },
    "15646002": {
        "Centro Poblado": "LA FABRICA"
    },
    "15660000": {
        "Centro Poblado": "SAN EDUARDO"
    },
    "15664000": {
        "Centro Poblado": "SAN JOSÉ DE PARE"
    },
    "15667000": {
        "Centro Poblado": "SAN LUIS DE GACENO"
    },
    "15667001": {
        "Centro Poblado": "SANTA TERESA"
    },
    "15667002": {
        "Centro Poblado": "GUAMAL"
    },
    "15667003": {
        "Centro Poblado": "HORIZONTES"
    },
    "15667004": {
        "Centro Poblado": "LA MESA DEL GUAVIO"
    },
    "15667005": {
        "Centro Poblado": "SAN CARLOS DEL GUAVIO"
    },
    "15667006": {
        "Centro Poblado": "LA FRONTERA (CORREDOR VIAL)"
    },
    "15673000": {
        "Centro Poblado": "SAN MATEO"
    },
    "15676000": {
        "Centro Poblado": "SAN MIGUEL DE SEMA"
    },
    "15681000": {
        "Centro Poblado": "SAN PABLO DE BORBUR"
    },
    "15681005": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "15681006": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "15681007": {
        "Centro Poblado": "COSCUEZ"
    },
    "15686000": {
        "Centro Poblado": "SANTANA"
    },
    "15686002": {
        "Centro Poblado": "CASABLANCA"
    },
    "15686003": {
        "Centro Poblado": "MATEGUADUA"
    },
    "15690000": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "15693000": {
        "Centro Poblado": "SANTA ROSA DE VITERBO"
    },
    "15693002": {
        "Centro Poblado": "EL IMPERIO"
    },
    "15696000": {
        "Centro Poblado": "SANTA SOFÍA"
    },
    "15720000": {
        "Centro Poblado": "SATIVANORTE"
    },
    "15720001": {
        "Centro Poblado": "SATIVA VIEJO"
    },
    "15723000": {
        "Centro Poblado": "SATIVASUR"
    },
    "15740000": {
        "Centro Poblado": "SIACHOQUE"
    },
    "15753000": {
        "Centro Poblado": "SOATÁ"
    },
    "15755000": {
        "Centro Poblado": "SOCOTÁ"
    },
    "15755004": {
        "Centro Poblado": "LOS PINOS"
    },
    "15757000": {
        "Centro Poblado": "SOCHA"
    },
    "15757001": {
        "Centro Poblado": "SANTA TERESA"
    },
    "15757003": {
        "Centro Poblado": "SOCHA VIEJO"
    },
    "15759000": {
        "Centro Poblado": "SOGAMOSO"
    },
    "15759001": {
        "Centro Poblado": "MORCÁ"
    },
    "15759003": {
        "Centro Poblado": "VANEGAS"
    },
    "15759005": {
        "Centro Poblado": "EL CRUCERO"
    },
    "15759006": {
        "Centro Poblado": "ALCAPARRAL"
    },
    "15759007": {
        "Centro Poblado": "MILAGRO Y PLAYITA"
    },
    "15761000": {
        "Centro Poblado": "SOMONDOCO"
    },
    "15762000": {
        "Centro Poblado": "SORA"
    },
    "15763000": {
        "Centro Poblado": "SOTAQUIRÁ"
    },
    "15763002": {
        "Centro Poblado": "BOSIGAS"
    },
    "15763003": {
        "Centro Poblado": "CARREÑO"
    },
    "15764000": {
        "Centro Poblado": "SORACÁ"
    },
    "15774000": {
        "Centro Poblado": "SUSACÓN"
    },
    "15776000": {
        "Centro Poblado": "SUTAMARCHÁN"
    },
    "15778000": {
        "Centro Poblado": "SUTATENZA"
    },
    "15790000": {
        "Centro Poblado": "TASCO"
    },
    "15790001": {
        "Centro Poblado": "LIBERTADORES"
    },
    "15790002": {
        "Centro Poblado": "LA CHAPA"
    },
    "15790003": {
        "Centro Poblado": "EL CASTILLO"
    },
    "15798000": {
        "Centro Poblado": "TENZA"
    },
    "15804000": {
        "Centro Poblado": "TIBANÁ"
    },
    "15806000": {
        "Centro Poblado": "TIBASOSA"
    },
    "15806002": {
        "Centro Poblado": "EL PARAÍSO"
    },
    "15806003": {
        "Centro Poblado": "SANTA TERESA"
    },
    "15808000": {
        "Centro Poblado": "TINJACÁ"
    },
    "15810000": {
        "Centro Poblado": "TIPACOQUE"
    },
    "15810005": {
        "Centro Poblado": "JEQUE"
    },
    "15814000": {
        "Centro Poblado": "TOCA"
    },
    "15816000": {
        "Centro Poblado": "TOGÜÍ"
    },
    "15820000": {
        "Centro Poblado": "TÓPAGA"
    },
    "15820001": {
        "Centro Poblado": "BADO CASTRO"
    },
    "15822000": {
        "Centro Poblado": "TOTA"
    },
    "15832000": {
        "Centro Poblado": "TUNUNGUÁ"
    },
    "15835000": {
        "Centro Poblado": "TURMEQUÉ"
    },
    "15837000": {
        "Centro Poblado": "TUTA"
    },
    "15839000": {
        "Centro Poblado": "TUTAZÁ"
    },
    "15839004": {
        "Centro Poblado": "LA CAPILLA"
    },
    "15842000": {
        "Centro Poblado": "ÚMBITA"
    },
    "15861000": {
        "Centro Poblado": "VENTAQUEMADA"
    },
    "15861001": {
        "Centro Poblado": "PARROQUIA VIEJA"
    },
    "15861002": {
        "Centro Poblado": "CASA VERDE"
    },
    "15861005": {
        "Centro Poblado": "MONTOYA"
    },
    "15861006": {
        "Centro Poblado": "ESTANCIA GRANDE"
    },
    "15861007": {
        "Centro Poblado": "PUENTE BOYACÁ"
    },
    "15861008": {
        "Centro Poblado": "TIERRA NEGRA"
    },
    "15861009": {
        "Centro Poblado": "EL CARPI"
    },
    "15861010": {
        "Centro Poblado": "EL MANZANO"
    },
    "15879000": {
        "Centro Poblado": "VIRACACHÁ"
    },
    "15897000": {
        "Centro Poblado": "ZETAQUIRA"
    },
    "17001000": {
        "Centro Poblado": "MANIZALES"
    },
    "17001001": {
        "Centro Poblado": "ALTO DE LISBOA"
    },
    "17001002": {
        "Centro Poblado": "KILOMETRO 41 - COLOMBIA"
    },
    "17001003": {
        "Centro Poblado": "BAJO TABLAZO"
    },
    "17001004": {
        "Centro Poblado": "LA CABAÑA"
    },
    "17001005": {
        "Centro Poblado": "LA CUCHILLA DEL SALADO"
    },
    "17001008": {
        "Centro Poblado": "LAS PAVAS"
    },
    "17001009": {
        "Centro Poblado": "SAN PEREGRINO"
    },
    "17001010": {
        "Centro Poblado": "ALTO TABLAZO"
    },
    "17001011": {
        "Centro Poblado": "ALTO DEL NARANJO"
    },
    "17001012": {
        "Centro Poblado": "EL ARENILLO"
    },
    "17001015": {
        "Centro Poblado": "LA AURORA"
    },
    "17001022": {
        "Centro Poblado": "ALTO BONITO"
    },
    "17001023": {
        "Centro Poblado": "MINA RICA"
    },
    "17001024": {
        "Centro Poblado": "LA GARRUCHA"
    },
    "17001029": {
        "Centro Poblado": "AGUA BONITA"
    },
    "17001034": {
        "Centro Poblado": "EL AGUILA"
    },
    "17001043": {
        "Centro Poblado": "BUENA VISTA"
    },
    "17001044": {
        "Centro Poblado": "CONDOMINIO PORTAL DE LOS CEREZOS"
    },
    "17001045": {
        "Centro Poblado": "CONDOMINIO RESERVA DE LOS ALAMOS"
    },
    "17001046": {
        "Centro Poblado": "CONDOMINIO SAN BERNARDO DEL VIENTO"
    },
    "17001047": {
        "Centro Poblado": "EL NARANJO"
    },
    "17013000": {
        "Centro Poblado": "AGUADAS"
    },
    "17013001": {
        "Centro Poblado": "ARMA"
    },
    "17013004": {
        "Centro Poblado": "LA MERMITA"
    },
    "17013010": {
        "Centro Poblado": "EDÉN"
    },
    "17013011": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "17013012": {
        "Centro Poblado": "ALTO DE PITO"
    },
    "17013014": {
        "Centro Poblado": "ALTO DE LA MONTAÑA"
    },
    "17013015": {
        "Centro Poblado": "BOCAS"
    },
    "17013016": {
        "Centro Poblado": "VIBORAL"
    },
    "17013017": {
        "Centro Poblado": "PORE"
    },
    "17042000": {
        "Centro Poblado": "ANSERMA"
    },
    "17042004": {
        "Centro Poblado": "MARAPRA"
    },
    "17042007": {
        "Centro Poblado": "SAN PEDRO"
    },
    "17042025": {
        "Centro Poblado": "CONDOMINIO LAS MARGARITAS"
    },
    "17050000": {
        "Centro Poblado": "ARANZAZU"
    },
    "17050006": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "17050012": {
        "Centro Poblado": "LA HONDA"
    },
    "17088000": {
        "Centro Poblado": "BELALCÁZAR"
    },
    "17088001": {
        "Centro Poblado": "EL MADROÑO"
    },
    "17088002": {
        "Centro Poblado": "LA HABANA"
    },
    "17088003": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "17088008": {
        "Centro Poblado": "ASENTAMIENTO INDÍGENA TOTUMAL"
    },
    "17174000": {
        "Centro Poblado": "CHINCHINÁ"
    },
    "17174001": {
        "Centro Poblado": "EL TRÉBOL"
    },
    "17174002": {
        "Centro Poblado": "LA FLORESTA"
    },
    "17174006": {
        "Centro Poblado": "ALTO DE LA MINA"
    },
    "17174007": {
        "Centro Poblado": "LA QUIEBRA DEL NARANJAL"
    },
    "17174011": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "17174012": {
        "Centro Poblado": "EL REPOSO"
    },
    "17174013": {
        "Centro Poblado": "GUAYABAL"
    },
    "17174015": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "17272000": {
        "Centro Poblado": "FILADELFIA"
    },
    "17272002": {
        "Centro Poblado": "EL VERSO"
    },
    "17272003": {
        "Centro Poblado": "LA PAILA"
    },
    "17272005": {
        "Centro Poblado": "SAMARIA"
    },
    "17272007": {
        "Centro Poblado": "SAN LUIS"
    },
    "17272008": {
        "Centro Poblado": "BALMORAL"
    },
    "17272009": {
        "Centro Poblado": "LA MARINA"
    },
    "17380000": {
        "Centro Poblado": "LA DORADA"
    },
    "17380001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "17380002": {
        "Centro Poblado": "GUARINOCITO"
    },
    "17380003": {
        "Centro Poblado": "PURNIO"
    },
    "17380004": {
        "Centro Poblado": "LA ATARRAYA"
    },
    "17380007": {
        "Centro Poblado": "CAMELIAS"
    },
    "17380008": {
        "Centro Poblado": "DOÑA JUANA"
    },
    "17380009": {
        "Centro Poblado": "HORIZONTE"
    },
    "17380010": {
        "Centro Poblado": "LA AGUSTINA"
    },
    "17380012": {
        "Centro Poblado": "LA HABANA"
    },
    "17380015": {
        "Centro Poblado": "PROSOCIAL LA HUMAREDA"
    },
    "17388000": {
        "Centro Poblado": "LA MERCED"
    },
    "17388001": {
        "Centro Poblado": "EL LIMÓN"
    },
    "17388002": {
        "Centro Poblado": "LA FELISA"
    },
    "17388007": {
        "Centro Poblado": "LLANADAS"
    },
    "17388008": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "17388009": {
        "Centro Poblado": "EL TAMBOR"
    },
    "17433000": {
        "Centro Poblado": "MANZANARES"
    },
    "17433001": {
        "Centro Poblado": "AGUABONITA"
    },
    "17433003": {
        "Centro Poblado": "LA CEIBA"
    },
    "17433004": {
        "Centro Poblado": "LAS MARGARITAS"
    },
    "17433005": {
        "Centro Poblado": "LOS PLANES"
    },
    "17442000": {
        "Centro Poblado": "MARMATO"
    },
    "17442001": {
        "Centro Poblado": "CABRAS"
    },
    "17442002": {
        "Centro Poblado": "EL LLANO"
    },
    "17442003": {
        "Centro Poblado": "SAN JUAN"
    },
    "17442004": {
        "Centro Poblado": "LA MIEL"
    },
    "17442005": {
        "Centro Poblado": "LA CUCHILLA"
    },
    "17442008": {
        "Centro Poblado": "JIMENEZ ALTO"
    },
    "17442009": {
        "Centro Poblado": "JIMENEZ BAJO"
    },
    "17442012": {
        "Centro Poblado": "LOAIZA"
    },
    "17442013": {
        "Centro Poblado": "EL GUAYABITO"
    },
    "17442014": {
        "Centro Poblado": "LA PORTADA"
    },
    "17442015": {
        "Centro Poblado": "LA QUEBRADA"
    },
    "17444000": {
        "Centro Poblado": "MARQUETALIA"
    },
    "17444001": {
        "Centro Poblado": "SANTA ELENA"
    },
    "17446000": {
        "Centro Poblado": "MARULANDA"
    },
    "17446001": {
        "Centro Poblado": "MONTEBONITO"
    },
    "17486000": {
        "Centro Poblado": "NEIRA"
    },
    "17486004": {
        "Centro Poblado": "PUEBLO RICO"
    },
    "17486005": {
        "Centro Poblado": "TAPIAS"
    },
    "17486009": {
        "Centro Poblado": "BARRIO MEDELLÍN"
    },
    "17486010": {
        "Centro Poblado": "LA ISLA"
    },
    "17486011": {
        "Centro Poblado": "AGROVILLA"
    },
    "17486012": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "17486013": {
        "Centro Poblado": "JUNTAS"
    },
    "17495000": {
        "Centro Poblado": "NORCASIA"
    },
    "17495002": {
        "Centro Poblado": "LA QUIEBRA"
    },
    "17495003": {
        "Centro Poblado": "MONTEBELLO"
    },
    "17495004": {
        "Centro Poblado": "MOSCOVITA"
    },
    "17513000": {
        "Centro Poblado": "PÁCORA"
    },
    "17513001": {
        "Centro Poblado": "CASTILLA"
    },
    "17513002": {
        "Centro Poblado": "LAS COLES"
    },
    "17513003": {
        "Centro Poblado": "SAN BARTOLOMÉ"
    },
    "17513008": {
        "Centro Poblado": "LOMA HERMOSA"
    },
    "17513011": {
        "Centro Poblado": "PALMA ALTA"
    },
    "17513012": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "17513013": {
        "Centro Poblado": "EL MORRO"
    },
    "17513016": {
        "Centro Poblado": "LOS CÁMBULOS"
    },
    "17524000": {
        "Centro Poblado": "PALESTINA"
    },
    "17524001": {
        "Centro Poblado": "ARAUCA"
    },
    "17524002": {
        "Centro Poblado": "EL JARDÍN (REPOSO)"
    },
    "17524003": {
        "Centro Poblado": "LA PLATA"
    },
    "17524005": {
        "Centro Poblado": "CARTAGENA"
    },
    "17524006": {
        "Centro Poblado": "SANTÁGUEDA"
    },
    "17524009": {
        "Centro Poblado": "LA BASTILLA"
    },
    "17541000": {
        "Centro Poblado": "PENSILVANIA"
    },
    "17541001": {
        "Centro Poblado": "ARBOLEDA"
    },
    "17541002": {
        "Centro Poblado": "BOLIVIA"
    },
    "17541004": {
        "Centro Poblado": "EL HIGUERÓN"
    },
    "17541006": {
        "Centro Poblado": "LA LINDA"
    },
    "17541008": {
        "Centro Poblado": "LA RIOJA"
    },
    "17541009": {
        "Centro Poblado": "PUEBLONUEVO"
    },
    "17541011": {
        "Centro Poblado": "SAN DANIEL"
    },
    "17541015": {
        "Centro Poblado": "LA SOLEDAD ALTA"
    },
    "17541016": {
        "Centro Poblado": "AGUABONITA"
    },
    "17614000": {
        "Centro Poblado": "RIOSUCIO"
    },
    "17614001": {
        "Centro Poblado": "BONAFONT"
    },
    "17614003": {
        "Centro Poblado": "EL SALADO"
    },
    "17614004": {
        "Centro Poblado": "FLORENCIA"
    },
    "17614005": {
        "Centro Poblado": "QUIEBRALOMO"
    },
    "17614006": {
        "Centro Poblado": "SAN LORENZO"
    },
    "17614008": {
        "Centro Poblado": "IBERIA"
    },
    "17614010": {
        "Centro Poblado": "SIPIRRA"
    },
    "17614014": {
        "Centro Poblado": "SAN JERÓNIMO"
    },
    "17614017": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "17614021": {
        "Centro Poblado": "LAS ESTANCIAS"
    },
    "17614022": {
        "Centro Poblado": "LA PLAYA - IMURRA"
    },
    "17614023": {
        "Centro Poblado": "TUMBABARRETO"
    },
    "17614024": {
        "Centro Poblado": "AGUAS CLARAS"
    },
    "17616000": {
        "Centro Poblado": "RISARALDA"
    },
    "17616004": {
        "Centro Poblado": "QUIEBRA SANTA BÁRBARA"
    },
    "17616008": {
        "Centro Poblado": "QUIEBRA VARILLAS"
    },
    "17616011": {
        "Centro Poblado": "CALLE LARGA"
    },
    "17653000": {
        "Centro Poblado": "SALAMINA"
    },
    "17653004": {
        "Centro Poblado": "VEREDA LA UNION"
    },
    "17653007": {
        "Centro Poblado": "SAN FÉLIX"
    },
    "17653023": {
        "Centro Poblado": "LA LOMA"
    },
    "17662000": {
        "Centro Poblado": "SAMANÁ"
    },
    "17662001": {
        "Centro Poblado": "BERLÍN"
    },
    "17662003": {
        "Centro Poblado": "FLORENCIA"
    },
    "17662004": {
        "Centro Poblado": "ENCIMADAS"
    },
    "17662005": {
        "Centro Poblado": "LOS POMOS"
    },
    "17662007": {
        "Centro Poblado": "SAN DIEGO"
    },
    "17662008": {
        "Centro Poblado": "RANCHOLARGO"
    },
    "17662017": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "17662018": {
        "Centro Poblado": "DULCE NOMBRE"
    },
    "17665000": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "17665002": {
        "Centro Poblado": "PRIMAVERA ALTA"
    },
    "17665004": {
        "Centro Poblado": "CONDOMINIOS VALLES DE ACAPULCO Y LOS SEIS Y PUNTO"
    },
    "17777000": {
        "Centro Poblado": "SUPÍA"
    },
    "17777003": {
        "Centro Poblado": "LA QUINTA"
    },
    "17777005": {
        "Centro Poblado": "HOJAS ANCHAS"
    },
    "17777008": {
        "Centro Poblado": "GUAMAL"
    },
    "17777010": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "17777011": {
        "Centro Poblado": "PALMA SOLA"
    },
    "17867000": {
        "Centro Poblado": "VICTORIA"
    },
    "17867001": {
        "Centro Poblado": "CAÑAVERAL"
    },
    "17867003": {
        "Centro Poblado": "ISAZA"
    },
    "17867004": {
        "Centro Poblado": "LA PRADERA"
    },
    "17867005": {
        "Centro Poblado": "EL LLANO"
    },
    "17867007": {
        "Centro Poblado": "LA FE"
    },
    "17867008": {
        "Centro Poblado": "SAN MATEO"
    },
    "17867009": {
        "Centro Poblado": "VILLA ESPERANZA"
    },
    "17873000": {
        "Centro Poblado": "VILLAMARÍA"
    },
    "17873001": {
        "Centro Poblado": "ALTO DE LA CRUZ - LOS CUERVOS"
    },
    "17873003": {
        "Centro Poblado": "LLANITOS"
    },
    "17873004": {
        "Centro Poblado": "RIOCLARO"
    },
    "17873006": {
        "Centro Poblado": "SAN JULIÁN"
    },
    "17873007": {
        "Centro Poblado": "MIRAFLORES"
    },
    "17873008": {
        "Centro Poblado": "ALTO VILLARAZO"
    },
    "17873010": {
        "Centro Poblado": "GALLINAZO"
    },
    "17873011": {
        "Centro Poblado": "LA NUEVA PRIMAVERA"
    },
    "17873013": {
        "Centro Poblado": "BELLAVISTA"
    },
    "17873014": {
        "Centro Poblado": "LA FLORESTA"
    },
    "17873016": {
        "Centro Poblado": "COROZAL"
    },
    "17873017": {
        "Centro Poblado": "PARTIDAS"
    },
    "17873018": {
        "Centro Poblado": "GRANJA AGRÍCOLA LA PAZ"
    },
    "17873019": {
        "Centro Poblado": "NUEVO RÍO CLARO"
    },
    "17877000": {
        "Centro Poblado": "VITERBO"
    },
    "18001000": {
        "Centro Poblado": "FLORENCIA"
    },
    "18001004": {
        "Centro Poblado": "SAN ANTONIO DE ATENAS"
    },
    "18001005": {
        "Centro Poblado": "SANTANA LAS HERMOSAS"
    },
    "18001006": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "18001007": {
        "Centro Poblado": "NORCACIA"
    },
    "18001008": {
        "Centro Poblado": "VENECIA"
    },
    "18001009": {
        "Centro Poblado": "EL PARA"
    },
    "18001011": {
        "Centro Poblado": "CARAÑO"
    },
    "18001018": {
        "Centro Poblado": "CAPITOLIO"
    },
    "18001024": {
        "Centro Poblado": "PUERTO ARANGO"
    },
    "18001025": {
        "Centro Poblado": "SEBASTOPOL"
    },
    "18029000": {
        "Centro Poblado": "ALBANIA"
    },
    "18029003": {
        "Centro Poblado": "DORADO"
    },
    "18029004": {
        "Centro Poblado": "VERSALLES"
    },
    "18029005": {
        "Centro Poblado": "EL PARAÍSO"
    },
    "18094000": {
        "Centro Poblado": "BELÉN DE LOS ANDAQUÍES"
    },
    "18094001": {
        "Centro Poblado": "EL PORTAL LA MONO"
    },
    "18094003": {
        "Centro Poblado": "PUERTO TORRES"
    },
    "18094005": {
        "Centro Poblado": "PUEBLO NUEVO LOS ÁNGELES"
    },
    "18094008": {
        "Centro Poblado": "ALETONES"
    },
    "18094009": {
        "Centro Poblado": "SAN ANTONIO DE PADUA"
    },
    "18150000": {
        "Centro Poblado": "CARTAGENA DEL CHAIRÁ"
    },
    "18150001": {
        "Centro Poblado": "REMOLINO DEL CAGUÁN"
    },
    "18150002": {
        "Centro Poblado": "SANTA FE DEL CAGUÁN"
    },
    "18150003": {
        "Centro Poblado": "MONSERRATE"
    },
    "18150004": {
        "Centro Poblado": "PEÑAS COLORADAS"
    },
    "18150005": {
        "Centro Poblado": "EL GUAMO"
    },
    "18150006": {
        "Centro Poblado": "PUERTO CAMELIA"
    },
    "18150007": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "18150008": {
        "Centro Poblado": "LOS CRISTALES"
    },
    "18150009": {
        "Centro Poblado": "RISARALDA"
    },
    "18150011": {
        "Centro Poblado": "CUMARALES"
    },
    "18150012": {
        "Centro Poblado": "EL CAFÉ"
    },
    "18150013": {
        "Centro Poblado": "NÁPOLES (PUERTO NÁPOLES)"
    },
    "18150014": {
        "Centro Poblado": "PEÑAS BLANCAS"
    },
    "18150015": {
        "Centro Poblado": "LAS ÁNIMAS"
    },
    "18205000": {
        "Centro Poblado": "CURILLO"
    },
    "18205001": {
        "Centro Poblado": "SALAMINA"
    },
    "18205002": {
        "Centro Poblado": "NOVIA PUERTO VALDIVIA"
    },
    "18205003": {
        "Centro Poblado": "PALIZADAS"
    },
    "18247000": {
        "Centro Poblado": "EL DONCELLO"
    },
    "18247001": {
        "Centro Poblado": "MAGUARE"
    },
    "18247002": {
        "Centro Poblado": "PUERTO MANRIQUE"
    },
    "18247004": {
        "Centro Poblado": "PUERTO HUNGRÍA"
    },
    "18247005": {
        "Centro Poblado": "RIONEGRO"
    },
    "18256000": {
        "Centro Poblado": "EL PAUJÍL"
    },
    "18256001": {
        "Centro Poblado": "VERSALLES"
    },
    "18256002": {
        "Centro Poblado": "BOLIVIA"
    },
    "18410000": {
        "Centro Poblado": "LA MONTAÑITA"
    },
    "18410001": {
        "Centro Poblado": "SANTUARIO"
    },
    "18410002": {
        "Centro Poblado": "LA UNIÓN PENEYA"
    },
    "18410005": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "18410006": {
        "Centro Poblado": "MATEGUADUA"
    },
    "18410007": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "18410008": {
        "Centro Poblado": "MIRAMAR"
    },
    "18410009": {
        "Centro Poblado": "PUERTO BRASILIA"
    },
    "18410010": {
        "Centro Poblado": "PUERTO GAITÁN"
    },
    "18410012": {
        "Centro Poblado": "REINA BAJA"
    },
    "18410013": {
        "Centro Poblado": "PALMERAS"
    },
    "18410014": {
        "Centro Poblado": "EL BERLIN"
    },
    "18460000": {
        "Centro Poblado": "MILÁN"
    },
    "18460001": {
        "Centro Poblado": "SAN ANTONIO DE GETUCHA"
    },
    "18460003": {
        "Centro Poblado": "MATICURU - GRANARIO"
    },
    "18460004": {
        "Centro Poblado": "LA RASTRA"
    },
    "18460005": {
        "Centro Poblado": "REMOLINOS DE ARICUNTÍ"
    },
    "18460008": {
        "Centro Poblado": "AGUA BLANCA"
    },
    "18460010": {
        "Centro Poblado": "AGUA NEGRA"
    },
    "18479000": {
        "Centro Poblado": "MORELIA"
    },
    "18592000": {
        "Centro Poblado": "PUERTO RICO"
    },
    "18592003": {
        "Centro Poblado": "LUSITANIA"
    },
    "18592004": {
        "Centro Poblado": "SANTANA RAMOS"
    },
    "18592005": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "18592006": {
        "Centro Poblado": "LA AGUILILLA"
    },
    "18610000": {
        "Centro Poblado": "SAN JOSÉ DEL FRAGUA"
    },
    "18610001": {
        "Centro Poblado": "FRAGUITA"
    },
    "18610002": {
        "Centro Poblado": "YURAYACO"
    },
    "18610003": {
        "Centro Poblado": "SABALETA"
    },
    "18753000": {
        "Centro Poblado": "SAN VICENTE DEL CAGUÁN"
    },
    "18753002": {
        "Centro Poblado": "GUACAMAYAS"
    },
    "18753003": {
        "Centro Poblado": "BALSILLAS"
    },
    "18753004": {
        "Centro Poblado": "CAMPO HERMOSO"
    },
    "18753007": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "18753009": {
        "Centro Poblado": "PUERTO BETANIA"
    },
    "18753010": {
        "Centro Poblado": "GIBRALTAR"
    },
    "18753011": {
        "Centro Poblado": "LOS POZOS"
    },
    "18753012": {
        "Centro Poblado": "SANTA ROSA"
    },
    "18753013": {
        "Centro Poblado": "TRONCALES"
    },
    "18753015": {
        "Centro Poblado": "GUAYABAL"
    },
    "18753023": {
        "Centro Poblado": "LA TUNIA"
    },
    "18753029": {
        "Centro Poblado": "LA CAMPANA"
    },
    "18753031": {
        "Centro Poblado": "LOS ANDES"
    },
    "18753032": {
        "Centro Poblado": "PUERTO AMOR"
    },
    "18753033": {
        "Centro Poblado": "VILLA LOBOS"
    },
    "18753034": {
        "Centro Poblado": "VILLA CARMONA"
    },
    "18756000": {
        "Centro Poblado": "SOLANO"
    },
    "18756001": {
        "Centro Poblado": "ARARACUARA"
    },
    "18756004": {
        "Centro Poblado": "EL DANUBIO - CAMPO ALEGRE"
    },
    "18756005": {
        "Centro Poblado": "PEÑAS BLANCAS"
    },
    "18756006": {
        "Centro Poblado": "CUEMANI"
    },
    "18756007": {
        "Centro Poblado": "MONONGUETE"
    },
    "18756008": {
        "Centro Poblado": "PUERTO TEJADA"
    },
    "18756011": {
        "Centro Poblado": "PUERTO LAS MERCEDES"
    },
    "18785000": {
        "Centro Poblado": "SOLITA"
    },
    "18785001": {
        "Centro Poblado": "KILÓMETRO 28 (LA ARGELIA)"
    },
    "18785002": {
        "Centro Poblado": "KILÓMETRO 30 (CAMPO LEJANO)"
    },
    "18785005": {
        "Centro Poblado": "UNIÓN SINCELEJO"
    },
    "18860000": {
        "Centro Poblado": "VALPARAÍSO"
    },
    "18860001": {
        "Centro Poblado": "SANTIAGO DE LA SELVA"
    },
    "18860002": {
        "Centro Poblado": "KILÓMETRO 18"
    },
    "18860005": {
        "Centro Poblado": "PLAYA RICA"
    },
    "19001000": {
        "Centro Poblado": "POPAYÁN"
    },
    "19001001": {
        "Centro Poblado": "CAJETE"
    },
    "19001002": {
        "Centro Poblado": "CALIBÍO"
    },
    "19001007": {
        "Centro Poblado": "JULUMITO"
    },
    "19001008": {
        "Centro Poblado": "LA REJOYA"
    },
    "19001013": {
        "Centro Poblado": "PUEBLILLO"
    },
    "19001014": {
        "Centro Poblado": "PUELENJE"
    },
    "19001019": {
        "Centro Poblado": "SANTA ROSA"
    },
    "19001025": {
        "Centro Poblado": "POBLAZÓN"
    },
    "19001026": {
        "Centro Poblado": "SAMUEL SILVERIO"
    },
    "19001027": {
        "Centro Poblado": "CRUCERO DE PUELENJE"
    },
    "19001028": {
        "Centro Poblado": "EL SALVADOR"
    },
    "19001029": {
        "Centro Poblado": "EL TÚNEL"
    },
    "19001030": {
        "Centro Poblado": "JULUMITO ALTO"
    },
    "19001031": {
        "Centro Poblado": "LA CABUYERA"
    },
    "19001032": {
        "Centro Poblado": "LA PLAYA"
    },
    "19001033": {
        "Centro Poblado": "LAME"
    },
    "19001034": {
        "Centro Poblado": "RÍO BLANCO"
    },
    "19001035": {
        "Centro Poblado": "VEREDA DE TORRES"
    },
    "19001037": {
        "Centro Poblado": "LA ESPERANZA (JARDINES DE PAZ)"
    },
    "19001038": {
        "Centro Poblado": "LA FORTALEZA"
    },
    "19001039": {
        "Centro Poblado": "PARCELACIÓN ATARDECERES DE LA PRADERA"
    },
    "19001040": {
        "Centro Poblado": "LOS LLANOS"
    },
    "19001041": {
        "Centro Poblado": "LAS PALMAS"
    },
    "19022000": {
        "Centro Poblado": "ALMAGUER"
    },
    "19022001": {
        "Centro Poblado": "CAQUIONA"
    },
    "19022003": {
        "Centro Poblado": "TABLÓN"
    },
    "19022004": {
        "Centro Poblado": "LLACUANAS"
    },
    "19022013": {
        "Centro Poblado": "SAN JORGE HERRADURA"
    },
    "19022014": {
        "Centro Poblado": "LA HONDA"
    },
    "19050000": {
        "Centro Poblado": "ARGELIA"
    },
    "19050001": {
        "Centro Poblado": "EL MANGO"
    },
    "19050002": {
        "Centro Poblado": "LA BELLEZA"
    },
    "19050005": {
        "Centro Poblado": "EL DIVISO"
    },
    "19050006": {
        "Centro Poblado": "EL PLATEADO"
    },
    "19050007": {
        "Centro Poblado": "SINAÍ"
    },
    "19050016": {
        "Centro Poblado": "PUERTO RICO"
    },
    "19050017": {
        "Centro Poblado": "SAN JUAN GUADUA"
    },
    "19075000": {
        "Centro Poblado": "BALBOA"
    },
    "19075001": {
        "Centro Poblado": "LA PLANADA"
    },
    "19075002": {
        "Centro Poblado": "OLAYA"
    },
    "19075003": {
        "Centro Poblado": "SAN ALFONSO"
    },
    "19075005": {
        "Centro Poblado": "LA BERMEJA"
    },
    "19075006": {
        "Centro Poblado": "PURETO"
    },
    "19075008": {
        "Centro Poblado": "LA LOMITA"
    },
    "19075009": {
        "Centro Poblado": "EL VIJAL"
    },
    "19075011": {
        "Centro Poblado": "PARAÍSO"
    },
    "19100000": {
        "Centro Poblado": "BOLÍVAR"
    },
    "19100001": {
        "Centro Poblado": "CAPELLANÍAS"
    },
    "19100005": {
        "Centro Poblado": "EL CARMEN"
    },
    "19100006": {
        "Centro Poblado": "EL RODEO"
    },
    "19100007": {
        "Centro Poblado": "GUACHICONO"
    },
    "19100013": {
        "Centro Poblado": "LERMA"
    },
    "19100015": {
        "Centro Poblado": "LOS MILAGROS"
    },
    "19100018": {
        "Centro Poblado": "MELCHOR"
    },
    "19100020": {
        "Centro Poblado": "SAN JUAN"
    },
    "19100021": {
        "Centro Poblado": "SAN LORENZO"
    },
    "19100041": {
        "Centro Poblado": "LA CARBONERA"
    },
    "19100042": {
        "Centro Poblado": "EL MORRO"
    },
    "19110000": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "19110006": {
        "Centro Poblado": "EL PORVENIR"
    },
    "19110007": {
        "Centro Poblado": "HONDURAS"
    },
    "19110008": {
        "Centro Poblado": "LA BALSA"
    },
    "19110012": {
        "Centro Poblado": "TIMBA"
    },
    "19110013": {
        "Centro Poblado": "EL CERAL"
    },
    "19110016": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "19110025": {
        "Centro Poblado": "PALOBLANCO"
    },
    "19110029": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "19110030": {
        "Centro Poblado": "MUNCHIQUE"
    },
    "19130000": {
        "Centro Poblado": "CAJIBÍO"
    },
    "19130004": {
        "Centro Poblado": "EL CARMELO"
    },
    "19130005": {
        "Centro Poblado": "EL ROSARIO"
    },
    "19130006": {
        "Centro Poblado": "LA CAPILLA"
    },
    "19130007": {
        "Centro Poblado": "LA PEDREGOSA"
    },
    "19130008": {
        "Centro Poblado": "LA VENTA"
    },
    "19130009": {
        "Centro Poblado": "SANTA TERESA DE CASAS BAJAS"
    },
    "19130010": {
        "Centro Poblado": "ORTEGA"
    },
    "19130017": {
        "Centro Poblado": "EL CAIRO"
    },
    "19130018": {
        "Centro Poblado": "EL COFRE"
    },
    "19130019": {
        "Centro Poblado": "ISLA DEL PONTON"
    },
    "19130020": {
        "Centro Poblado": "LA LAGUNA DINDE"
    },
    "19130021": {
        "Centro Poblado": "RESGUARDO INDÍGENA DEL GUAYABAL CXAYUGE FXIW CXAB"
    },
    "19130022": {
        "Centro Poblado": "URBANIZACIÓN LAS MARGARITAS"
    },
    "19137000": {
        "Centro Poblado": "CALDONO"
    },
    "19137001": {
        "Centro Poblado": "CERRO ALTO"
    },
    "19137002": {
        "Centro Poblado": "EL PITAL"
    },
    "19137004": {
        "Centro Poblado": "PESCADOR"
    },
    "19137007": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "19137008": {
        "Centro Poblado": "SIBERIA"
    },
    "19137013": {
        "Centro Poblado": "CRUCERO DE PESCADOR"
    },
    "19142000": {
        "Centro Poblado": "CALOTO"
    },
    "19142004": {
        "Centro Poblado": "EL PALO"
    },
    "19142007": {
        "Centro Poblado": "HUASANÓ"
    },
    "19142011": {
        "Centro Poblado": "QUINTERO"
    },
    "19142015": {
        "Centro Poblado": "LA ARROBLEDA"
    },
    "19142030": {
        "Centro Poblado": "CRUCERO DE GUALÍ"
    },
    "19142031": {
        "Centro Poblado": "HUELLAS"
    },
    "19142032": {
        "Centro Poblado": "ALTO EL PALO"
    },
    "19142034": {
        "Centro Poblado": "BODEGA ARRIBA"
    },
    "19142038": {
        "Centro Poblado": "EL NILO"
    },
    "19142039": {
        "Centro Poblado": "EL GUÁSIMO"
    },
    "19142045": {
        "Centro Poblado": "TOEZ"
    },
    "19142050": {
        "Centro Poblado": "LÓPEZ ADENTRO"
    },
    "19142051": {
        "Centro Poblado": "MORALES"
    },
    "19142056": {
        "Centro Poblado": "PÍLAMO"
    },
    "19212000": {
        "Centro Poblado": "CORINTO"
    },
    "19212001": {
        "Centro Poblado": "EL JAGUAL"
    },
    "19212004": {
        "Centro Poblado": "MEDIA NARANJA"
    },
    "19212005": {
        "Centro Poblado": "RIONEGRO"
    },
    "19212008": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "19212009": {
        "Centro Poblado": "EL BARRANCO"
    },
    "19212010": {
        "Centro Poblado": "QUEBRADITAS"
    },
    "19256000": {
        "Centro Poblado": "EL TAMBO"
    },
    "19256001": {
        "Centro Poblado": "ALTO DEL REY"
    },
    "19256004": {
        "Centro Poblado": "CUATRO ESQUINAS"
    },
    "19256005": {
        "Centro Poblado": "CHAPA"
    },
    "19256007": {
        "Centro Poblado": "EL PLACER"
    },
    "19256009": {
        "Centro Poblado": "EL ZARZAL"
    },
    "19256012": {
        "Centro Poblado": "HUISITÓ"
    },
    "19256013": {
        "Centro Poblado": "LA ALIANZA"
    },
    "19256014": {
        "Centro Poblado": "LA PAZ"
    },
    "19256015": {
        "Centro Poblado": "LOS ANAYES"
    },
    "19256016": {
        "Centro Poblado": "LOS ANDES"
    },
    "19256019": {
        "Centro Poblado": "PANDIGUANDO"
    },
    "19256020": {
        "Centro Poblado": "PIAGUA"
    },
    "19256022": {
        "Centro Poblado": "QUILCACÉ"
    },
    "19256025": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "19256027": {
        "Centro Poblado": "SEGUENGUE"
    },
    "19256028": {
        "Centro Poblado": "URIBE"
    },
    "19256029": {
        "Centro Poblado": "FONDAS"
    },
    "19256031": {
        "Centro Poblado": "BUENA VISTA"
    },
    "19256032": {
        "Centro Poblado": "LAS BOTAS"
    },
    "19256033": {
        "Centro Poblado": "CABUYAL"
    },
    "19256034": {
        "Centro Poblado": "EL CRUCERO DEL PUEBLO"
    },
    "19256036": {
        "Centro Poblado": "PLAYA RICA"
    },
    "19256058": {
        "Centro Poblado": "AIRES DE OCCIDENTE"
    },
    "19256059": {
        "Centro Poblado": "EL CRUCERO DE PANDIGUANDO"
    },
    "19256060": {
        "Centro Poblado": "EL RECUERDO"
    },
    "19256061": {
        "Centro Poblado": "LA CHICUEÑA"
    },
    "19256062": {
        "Centro Poblado": "PUENTE DEL RÍO TIMBIO"
    },
    "19290000": {
        "Centro Poblado": "FLORENCIA"
    },
    "19290001": {
        "Centro Poblado": "EL ROSARIO"
    },
    "19290002": {
        "Centro Poblado": "MARSELLA"
    },
    "19300000": {
        "Centro Poblado": "GUACHENÉ"
    },
    "19300004": {
        "Centro Poblado": "BARRAGAN"
    },
    "19300005": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "19300006": {
        "Centro Poblado": "CAPONERA 1"
    },
    "19300007": {
        "Centro Poblado": "CAPONERA SECTOR PALO BLANCO"
    },
    "19300008": {
        "Centro Poblado": "CIENAGA HONDA"
    },
    "19300009": {
        "Centro Poblado": "GUABAL"
    },
    "19300010": {
        "Centro Poblado": "GUABAL 1"
    },
    "19300011": {
        "Centro Poblado": "GUABAL 2"
    },
    "19300012": {
        "Centro Poblado": "LA CABAÑA"
    },
    "19300013": {
        "Centro Poblado": "LA CABAÑITA"
    },
    "19300014": {
        "Centro Poblado": "LA DOMINGA"
    },
    "19300015": {
        "Centro Poblado": "LLANO DE TAULA ALTO"
    },
    "19300016": {
        "Centro Poblado": "LLANO DE TAULA BAJO"
    },
    "19300017": {
        "Centro Poblado": "MINGO"
    },
    "19300018": {
        "Centro Poblado": "OBANDO"
    },
    "19300019": {
        "Centro Poblado": "OBANDO SECTOR LA ESPERANZA"
    },
    "19300020": {
        "Centro Poblado": "SABANETA"
    },
    "19300021": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "19300022": {
        "Centro Poblado": "SAN JACINTO"
    },
    "19300023": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "19318000": {
        "Centro Poblado": "GUAPI"
    },
    "19318002": {
        "Centro Poblado": "BENJAMÍN HERRERA (SAN VICENTE)"
    },
    "19318003": {
        "Centro Poblado": "CALLELARGA"
    },
    "19318005": {
        "Centro Poblado": "EL CARMELO"
    },
    "19318008": {
        "Centro Poblado": "LIMONES"
    },
    "19318011": {
        "Centro Poblado": "EL ROSARIO"
    },
    "19318012": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "19318013": {
        "Centro Poblado": "SAN ANTONIO DE GUAJUÍ"
    },
    "19318015": {
        "Centro Poblado": "URIBE URIBE (EL NARANJO)"
    },
    "19318024": {
        "Centro Poblado": "QUIROGA"
    },
    "19318025": {
        "Centro Poblado": "CHUARE"
    },
    "19318026": {
        "Centro Poblado": "SAN JOSE DE GUARE"
    },
    "19318027": {
        "Centro Poblado": "BELÉN"
    },
    "19318028": {
        "Centro Poblado": "CAIMITO"
    },
    "19318029": {
        "Centro Poblado": "SANTA ANA"
    },
    "19355000": {
        "Centro Poblado": "INZÁ"
    },
    "19355001": {
        "Centro Poblado": "CALDERAS"
    },
    "19355002": {
        "Centro Poblado": "PEDREGAL"
    },
    "19355003": {
        "Centro Poblado": "PUERTO VALENCIA"
    },
    "19355004": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "19355008": {
        "Centro Poblado": "TUMBICHUCUE"
    },
    "19355009": {
        "Centro Poblado": "TURMINÁ"
    },
    "19355016": {
        "Centro Poblado": "LA MILAGROSA"
    },
    "19355017": {
        "Centro Poblado": "YAQUIVÁ"
    },
    "19364000": {
        "Centro Poblado": "JAMBALÓ"
    },
    "19392000": {
        "Centro Poblado": "LA SIERRA"
    },
    "19392001": {
        "Centro Poblado": "LA DEPRESIÓN"
    },
    "19392005": {
        "Centro Poblado": "LA CUCHILLA"
    },
    "19392006": {
        "Centro Poblado": "LA CUCHILLA ALTA"
    },
    "19397000": {
        "Centro Poblado": "LA VEGA"
    },
    "19397001": {
        "Centro Poblado": "ALTAMIRA"
    },
    "19397002": {
        "Centro Poblado": "ARBELA"
    },
    "19397004": {
        "Centro Poblado": "EL PALMAR"
    },
    "19397005": {
        "Centro Poblado": "GUACHICONO"
    },
    "19397006": {
        "Centro Poblado": "LOS UVOS"
    },
    "19397007": {
        "Centro Poblado": "PANCITARÁ"
    },
    "19397009": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "19397010": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "19397011": {
        "Centro Poblado": "SANTA JUANA"
    },
    "19397012": {
        "Centro Poblado": "ALBANIA"
    },
    "19397018": {
        "Centro Poblado": "BARBILLAS"
    },
    "19397019": {
        "Centro Poblado": "SANTA RITA"
    },
    "19418000": {
        "Centro Poblado": "LÓPEZ"
    },
    "19418009": {
        "Centro Poblado": "NOANAMITO"
    },
    "19418010": {
        "Centro Poblado": "PLAYA GRANDE"
    },
    "19418012": {
        "Centro Poblado": "SAN ANTONIO DE CHUARE"
    },
    "19418018": {
        "Centro Poblado": "TAPARAL"
    },
    "19418019": {
        "Centro Poblado": "ZARAGOZA"
    },
    "19418024": {
        "Centro Poblado": "BETANIA"
    },
    "19418032": {
        "Centro Poblado": "SAN ANTONIO DE GURUMENDY"
    },
    "19418035": {
        "Centro Poblado": "SANTA CRUZ DE SIGUI"
    },
    "19418036": {
        "Centro Poblado": "CABECITAS"
    },
    "19418038": {
        "Centro Poblado": "ISLA DE GALLO"
    },
    "19418039": {
        "Centro Poblado": "JUAN COBO"
    },
    "19450000": {
        "Centro Poblado": "MERCADERES"
    },
    "19450002": {
        "Centro Poblado": "ARBOLEDAS"
    },
    "19450003": {
        "Centro Poblado": "EL PILÓN"
    },
    "19450004": {
        "Centro Poblado": "ESMERALDAS"
    },
    "19450006": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "19450007": {
        "Centro Poblado": "SAN JUANITO"
    },
    "19450010": {
        "Centro Poblado": "CURACAS"
    },
    "19450012": {
        "Centro Poblado": "LA DESPENSA"
    },
    "19450014": {
        "Centro Poblado": "SOMBRERILLOS"
    },
    "19450015": {
        "Centro Poblado": "EL BADO"
    },
    "19450016": {
        "Centro Poblado": "TABLONCITO"
    },
    "19450019": {
        "Centro Poblado": "MOJARRAS"
    },
    "19450020": {
        "Centro Poblado": "LOS LLANOS"
    },
    "19450023": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "19450024": {
        "Centro Poblado": "EL CANGREJO"
    },
    "19450025": {
        "Centro Poblado": "EL COCAL"
    },
    "19450026": {
        "Centro Poblado": "ESPERANZAS DE MAYO"
    },
    "19450027": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "19455000": {
        "Centro Poblado": "MIRANDA"
    },
    "19455005": {
        "Centro Poblado": "ORTIGAL"
    },
    "19455007": {
        "Centro Poblado": "SANTA ANA"
    },
    "19455008": {
        "Centro Poblado": "TIERRADURA"
    },
    "19455009": {
        "Centro Poblado": "TULIPAN"
    },
    "19455010": {
        "Centro Poblado": "GUATEMALA"
    },
    "19455011": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "19455013": {
        "Centro Poblado": "LA LINDOSA"
    },
    "19473000": {
        "Centro Poblado": "MORALES"
    },
    "19473002": {
        "Centro Poblado": "CARPINTERO"
    },
    "19473009": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "19473012": {
        "Centro Poblado": "SANTA ROSA"
    },
    "19473014": {
        "Centro Poblado": "LA ESTACIÓN"
    },
    "19473017": {
        "Centro Poblado": "EL ROSARIO"
    },
    "19513000": {
        "Centro Poblado": "PADILLA"
    },
    "19513001": {
        "Centro Poblado": "YARUMALES"
    },
    "19513003": {
        "Centro Poblado": "LA PAILA"
    },
    "19513004": {
        "Centro Poblado": "EL CHAMIZO"
    },
    "19513007": {
        "Centro Poblado": "LOS ROBLES"
    },
    "19513008": {
        "Centro Poblado": "CUERNAVACA"
    },
    "19517000": {
        "Centro Poblado": "BELALCÁZAR"
    },
    "19517002": {
        "Centro Poblado": "AVIRAMA"
    },
    "19517003": {
        "Centro Poblado": "COHETANDO"
    },
    "19517007": {
        "Centro Poblado": "ITAIBE"
    },
    "19517012": {
        "Centro Poblado": "RICAURTE"
    },
    "19517013": {
        "Centro Poblado": "RIOCHIQUITO"
    },
    "19517014": {
        "Centro Poblado": "SAN LUIS (POTRERILLO)"
    },
    "19517015": {
        "Centro Poblado": "TALAGA"
    },
    "19517016": {
        "Centro Poblado": "TÓEZ"
    },
    "19517017": {
        "Centro Poblado": "LA MESA DE TOGOIMA"
    },
    "19517029": {
        "Centro Poblado": "MINUTO DE DIOS"
    },
    "19517030": {
        "Centro Poblado": "COQUIYÓ"
    },
    "19517032": {
        "Centro Poblado": "EL RODEO"
    },
    "19517033": {
        "Centro Poblado": "GUADUALEJO"
    },
    "19517034": {
        "Centro Poblado": "GUAPIO"
    },
    "19517035": {
        "Centro Poblado": "GUAQUIYÓ"
    },
    "19517037": {
        "Centro Poblado": "LA MARÍA"
    },
    "19517039": {
        "Centro Poblado": "MESA DE CALOTO"
    },
    "19517040": {
        "Centro Poblado": "MESA DE TÁLAGA"
    },
    "19517043": {
        "Centro Poblado": "VICANENGA"
    },
    "19517044": {
        "Centro Poblado": "LA MESA DE AVIRAMA"
    },
    "19517045": {
        "Centro Poblado": "LA MESA DE BELALCAZAR"
    },
    "19517046": {
        "Centro Poblado": "SANTA ROSA"
    },
    "19532000": {
        "Centro Poblado": "EL BORDO"
    },
    "19532001": {
        "Centro Poblado": "BRISAS"
    },
    "19532003": {
        "Centro Poblado": "DON ALONSO"
    },
    "19532004": {
        "Centro Poblado": "GALÍNDEZ"
    },
    "19532005": {
        "Centro Poblado": "LA FONDA"
    },
    "19532006": {
        "Centro Poblado": "LA MESA"
    },
    "19532008": {
        "Centro Poblado": "PATÍA"
    },
    "19532009": {
        "Centro Poblado": "PIEDRASENTADA"
    },
    "19532010": {
        "Centro Poblado": "PAN DE AZÚCAR"
    },
    "19532012": {
        "Centro Poblado": "SAJANDÍ"
    },
    "19532013": {
        "Centro Poblado": "EL ESTRECHO"
    },
    "19532014": {
        "Centro Poblado": "EL HOYO"
    },
    "19532025": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "19532032": {
        "Centro Poblado": "PALO MOCHO"
    },
    "19533000": {
        "Centro Poblado": "PIAMONTE"
    },
    "19533002": {
        "Centro Poblado": "EL REMANSO"
    },
    "19533003": {
        "Centro Poblado": "MIRAFLOR"
    },
    "19533004": {
        "Centro Poblado": "YAPURÁ"
    },
    "19533005": {
        "Centro Poblado": "LAS PALMERAS 1"
    },
    "19533006": {
        "Centro Poblado": "LAS PALMERAS 2"
    },
    "19533007": {
        "Centro Poblado": "NÁPOLES"
    },
    "19548000": {
        "Centro Poblado": "PIENDAMÓ"
    },
    "19548001": {
        "Centro Poblado": "TUNÍA"
    },
    "19573000": {
        "Centro Poblado": "PUERTO TEJADA"
    },
    "19573001": {
        "Centro Poblado": "BOCAS DEL PALO"
    },
    "19573002": {
        "Centro Poblado": "LAS BRISAS"
    },
    "19573003": {
        "Centro Poblado": "SAN CARLOS"
    },
    "19573004": {
        "Centro Poblado": "ZANJÓN RICO"
    },
    "19573006": {
        "Centro Poblado": "VUELTA LARGA"
    },
    "19573008": {
        "Centro Poblado": "LOS BANCOS"
    },
    "19573009": {
        "Centro Poblado": "GUENGUE"
    },
    "19573010": {
        "Centro Poblado": "CIUDAD SUR"
    },
    "19585000": {
        "Centro Poblado": "COCONUCO"
    },
    "19585004": {
        "Centro Poblado": "PURACÉ"
    },
    "19585007": {
        "Centro Poblado": "SANTA LETICIA"
    },
    "19585008": {
        "Centro Poblado": "JUAN TAMA"
    },
    "19585009": {
        "Centro Poblado": "PALETARÁ"
    },
    "19585010": {
        "Centro Poblado": "CHAPÍO"
    },
    "19622000": {
        "Centro Poblado": "ROSAS"
    },
    "19622002": {
        "Centro Poblado": "PÁRRAGA"
    },
    "19622007": {
        "Centro Poblado": "CEFIRO"
    },
    "19622011": {
        "Centro Poblado": "SAUCE"
    },
    "19693000": {
        "Centro Poblado": "SAN SEBASTIÁN"
    },
    "19693001": {
        "Centro Poblado": "EL ROSAL"
    },
    "19693004": {
        "Centro Poblado": "SANTIAGO"
    },
    "19693005": {
        "Centro Poblado": "VALENCIA"
    },
    "19693006": {
        "Centro Poblado": "VENECIA"
    },
    "19698000": {
        "Centro Poblado": "SANTANDER DE QUILICHAO"
    },
    "19698001": {
        "Centro Poblado": "EL PALMAR"
    },
    "19698002": {
        "Centro Poblado": "EL TURCO"
    },
    "19698004": {
        "Centro Poblado": "LA ARROBLEDA"
    },
    "19698007": {
        "Centro Poblado": "MONDOMO"
    },
    "19698008": {
        "Centro Poblado": "PARAMILLO 1"
    },
    "19698009": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "19698010": {
        "Centro Poblado": "TRES QUEBRADAS"
    },
    "19698013": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "19698014": {
        "Centro Poblado": "SAN PEDRO"
    },
    "19698017": {
        "Centro Poblado": "DOMINGUILLO"
    },
    "19698018": {
        "Centro Poblado": "EL CRUCERO"
    },
    "19698020": {
        "Centro Poblado": "QUINAMAYO"
    },
    "19698022": {
        "Centro Poblado": "LLANO DE ALEGRÍAS"
    },
    "19698023": {
        "Centro Poblado": "CABECERA DOMINGUILLO"
    },
    "19698024": {
        "Centro Poblado": "CAMBALACHE"
    },
    "19698025": {
        "Centro Poblado": "EL BROCHE"
    },
    "19698026": {
        "Centro Poblado": "EL LLANITO"
    },
    "19698027": {
        "Centro Poblado": "EL TAJO"
    },
    "19698028": {
        "Centro Poblado": "LA AGUSTINA"
    },
    "19698029": {
        "Centro Poblado": "LA CAPILLA"
    },
    "19698030": {
        "Centro Poblado": "LA CHAPA"
    },
    "19698031": {
        "Centro Poblado": "LA PALOMERA"
    },
    "19698032": {
        "Centro Poblado": "LA QUEBRADA"
    },
    "19698033": {
        "Centro Poblado": "LOMITAS ABAJO"
    },
    "19698034": {
        "Centro Poblado": "LOMITAS ARRIBA"
    },
    "19698035": {
        "Centro Poblado": "LOURDES"
    },
    "19698036": {
        "Centro Poblado": "MANDIVA"
    },
    "19698037": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "19698042": {
        "Centro Poblado": "VILACHÍ"
    },
    "19698043": {
        "Centro Poblado": "BELLAVISTA"
    },
    "19698044": {
        "Centro Poblado": "PARAMILLO 2"
    },
    "19698045": {
        "Centro Poblado": "TERRITORIO NASA KIWETK LA MARÍA"
    },
    "19698046": {
        "Centro Poblado": "TERRITORIO NASA KIWE TEKH KSXAW"
    },
    "19701000": {
        "Centro Poblado": "SANTA ROSA"
    },
    "19701001": {
        "Centro Poblado": "DESCANSE"
    },
    "19701002": {
        "Centro Poblado": "EL CARMELO"
    },
    "19701006": {
        "Centro Poblado": "SAN JUAN DE VILLALOBOS"
    },
    "19743000": {
        "Centro Poblado": "SILVIA"
    },
    "19743002": {
        "Centro Poblado": "PITAYO"
    },
    "19743003": {
        "Centro Poblado": "QUICHAYÁ"
    },
    "19743005": {
        "Centro Poblado": "USENDA"
    },
    "19760000": {
        "Centro Poblado": "PAISPAMBA"
    },
    "19760001": {
        "Centro Poblado": "CHAPA"
    },
    "19760007": {
        "Centro Poblado": "RÍO BLANCO"
    },
    "19760012": {
        "Centro Poblado": "LAS VEGAS"
    },
    "19780000": {
        "Centro Poblado": "SUÁREZ"
    },
    "19780007": {
        "Centro Poblado": "LA TOMA"
    },
    "19780008": {
        "Centro Poblado": "LA BETULIA"
    },
    "19780011": {
        "Centro Poblado": "ALTAMIRA"
    },
    "19785000": {
        "Centro Poblado": "SUCRE"
    },
    "19785001": {
        "Centro Poblado": "EL PARAÍSO"
    },
    "19785008": {
        "Centro Poblado": "LA CEJA"
    },
    "19807000": {
        "Centro Poblado": "TIMBÍO"
    },
    "19807007": {
        "Centro Poblado": "CRUCES"
    },
    "19807009": {
        "Centro Poblado": "ALTO SAN JOSÉ"
    },
    "19807016": {
        "Centro Poblado": "LAS HUACAS"
    },
    "19809000": {
        "Centro Poblado": "TIMBIQUÍ"
    },
    "19809001": {
        "Centro Poblado": "BUBUEY"
    },
    "19809002": {
        "Centro Poblado": "CAMARONES"
    },
    "19809003": {
        "Centro Poblado": "COTEJE"
    },
    "19809006": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "19809007": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "19809008": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "19809009": {
        "Centro Poblado": "SANTA ROSA DE SAIJA"
    },
    "19809010": {
        "Centro Poblado": "CHETE"
    },
    "19809011": {
        "Centro Poblado": "BOCA DE PATÍA"
    },
    "19809012": {
        "Centro Poblado": "EL CHARCO"
    },
    "19809013": {
        "Centro Poblado": "EL REALITO"
    },
    "19809018": {
        "Centro Poblado": "CUPI"
    },
    "19809020": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "19809021": {
        "Centro Poblado": "COROZAL"
    },
    "19809022": {
        "Centro Poblado": "CABECITAL"
    },
    "19809023": {
        "Centro Poblado": "PUERTO SAIJA"
    },
    "19809024": {
        "Centro Poblado": "ANGOSTURA"
    },
    "19809025": {
        "Centro Poblado": "GUANGUI"
    },
    "19809026": {
        "Centro Poblado": "LOS BRASOS"
    },
    "19809027": {
        "Centro Poblado": "PIZARE"
    },
    "19821000": {
        "Centro Poblado": "TORIBÍO"
    },
    "19821005": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "19821007": {
        "Centro Poblado": "TACUEYO"
    },
    "19821009": {
        "Centro Poblado": "CALOTO NUEVO"
    },
    "19821010": {
        "Centro Poblado": "EL HUILA"
    },
    "19824000": {
        "Centro Poblado": "TOTORÓ"
    },
    "19824002": {
        "Centro Poblado": "GABRIEL LÓPEZ"
    },
    "19824004": {
        "Centro Poblado": "PANIQUITÁ"
    },
    "19845000": {
        "Centro Poblado": "VILLA RICA"
    },
    "19845005": {
        "Centro Poblado": "JUAN IGNACIO"
    },
    "19845006": {
        "Centro Poblado": "PRIMAVERA"
    },
    "19845007": {
        "Centro Poblado": "PERICO NEGRO"
    },
    "20001000": {
        "Centro Poblado": "VALLEDUPAR"
    },
    "20001001": {
        "Centro Poblado": "AGUAS BLANCAS"
    },
    "20001002": {
        "Centro Poblado": "ATANQUEZ"
    },
    "20001003": {
        "Centro Poblado": "BADILLO"
    },
    "20001005": {
        "Centro Poblado": "CARACOLÍ"
    },
    "20001006": {
        "Centro Poblado": "CHEMESQUEMENA"
    },
    "20001007": {
        "Centro Poblado": "GUATAPURÍ"
    },
    "20001009": {
        "Centro Poblado": "GUACOCHE"
    },
    "20001010": {
        "Centro Poblado": "GUAYMARAL"
    },
    "20001011": {
        "Centro Poblado": "LA MINA"
    },
    "20001012": {
        "Centro Poblado": "LOS VENADOS"
    },
    "20001013": {
        "Centro Poblado": "MARIANGOLA"
    },
    "20001014": {
        "Centro Poblado": "PATILLAL"
    },
    "20001018": {
        "Centro Poblado": "VALENCIA DE JESUS"
    },
    "20001019": {
        "Centro Poblado": "CAMPERUCHO"
    },
    "20001022": {
        "Centro Poblado": "GUACOCHITO"
    },
    "20001024": {
        "Centro Poblado": "LOS CALABAZOS"
    },
    "20001025": {
        "Centro Poblado": "LOS CORAZONES"
    },
    "20001026": {
        "Centro Poblado": "LOS HATICOS  I"
    },
    "20001027": {
        "Centro Poblado": "LA MESA - AZUCAR BUENA"
    },
    "20001028": {
        "Centro Poblado": "RAICES"
    },
    "20001030": {
        "Centro Poblado": "RANCHO DE GOYA"
    },
    "20001031": {
        "Centro Poblado": "RÍO SECO"
    },
    "20001032": {
        "Centro Poblado": "LA VEGA  ARRIBA"
    },
    "20001034": {
        "Centro Poblado": "VILLA GERMANIA"
    },
    "20001036": {
        "Centro Poblado": "EL JABO"
    },
    "20001037": {
        "Centro Poblado": "EL ALTO DE LA VUELTA"
    },
    "20001038": {
        "Centro Poblado": "HATICOS II"
    },
    "20001039": {
        "Centro Poblado": "EL PERRO"
    },
    "20001040": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "20001041": {
        "Centro Poblado": "SABANA DE CRESPO"
    },
    "20001042": {
        "Centro Poblado": "LAS CASITAS"
    },
    "20001044": {
        "Centro Poblado": "MARUAMAQUE"
    },
    "20001045": {
        "Centro Poblado": "PONTÓN"
    },
    "20001047": {
        "Centro Poblado": "EL MOJAO"
    },
    "20001048": {
        "Centro Poblado": "RAMALITO"
    },
    "20001051": {
        "Centro Poblado": "VILLA RUEDA"
    },
    "20011000": {
        "Centro Poblado": "AGUACHICA"
    },
    "20011001": {
        "Centro Poblado": "BARRANCALEBRIJA"
    },
    "20011006": {
        "Centro Poblado": "LOMA DE CORREDOR"
    },
    "20011009": {
        "Centro Poblado": "PUERTO PATIÑO"
    },
    "20011010": {
        "Centro Poblado": "BUTURAMA"
    },
    "20011011": {
        "Centro Poblado": "NOREAN"
    },
    "20011012": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "20011014": {
        "Centro Poblado": "VILLA DE SAN ANDRÉS"
    },
    "20011025": {
        "Centro Poblado": "EL JUNCAL"
    },
    "20011026": {
        "Centro Poblado": "LA CAMPANA"
    },
    "20011029": {
        "Centro Poblado": "LA YE"
    },
    "20013000": {
        "Centro Poblado": "AGUSTÍN CODAZZI"
    },
    "20013002": {
        "Centro Poblado": "CASACARA"
    },
    "20013003": {
        "Centro Poblado": "LLERASCA"
    },
    "20013006": {
        "Centro Poblado": "PUNTA ARRECHA"
    },
    "20013007": {
        "Centro Poblado": "SAN RAMÓN"
    },
    "20032000": {
        "Centro Poblado": "ASTREA"
    },
    "20032001": {
        "Centro Poblado": "ARJONA"
    },
    "20032003": {
        "Centro Poblado": "EL YUCAL"
    },
    "20032005": {
        "Centro Poblado": "SANTA CECILIA"
    },
    "20032006": {
        "Centro Poblado": "EL HEBRÓN"
    },
    "20032007": {
        "Centro Poblado": "EL JOBO"
    },
    "20032008": {
        "Centro Poblado": "LA Y"
    },
    "20032009": {
        "Centro Poblado": "MONTECRISTO"
    },
    "20032010": {
        "Centro Poblado": "NUEVA COLOMBIA"
    },
    "20045000": {
        "Centro Poblado": "BECERRIL"
    },
    "20045001": {
        "Centro Poblado": "ESTADOS UNIDOS"
    },
    "20045004": {
        "Centro Poblado": "LA GUAJIRITA"
    },
    "20060000": {
        "Centro Poblado": "BOSCONIA"
    },
    "20060004": {
        "Centro Poblado": "LOMA COLORADA"
    },
    "20060010": {
        "Centro Poblado": "PUERTO LAJAS"
    },
    "20175000": {
        "Centro Poblado": "CHIMICHAGUA"
    },
    "20175004": {
        "Centro Poblado": "CANDELARIA"
    },
    "20175005": {
        "Centro Poblado": "EL GUAMO"
    },
    "20175008": {
        "Centro Poblado": "LAS FLORES"
    },
    "20175009": {
        "Centro Poblado": "LAS VEGAS"
    },
    "20175010": {
        "Centro Poblado": "MANDINGUILLA"
    },
    "20175011": {
        "Centro Poblado": "SALOA"
    },
    "20175013": {
        "Centro Poblado": "SEMPEGUA"
    },
    "20175014": {
        "Centro Poblado": "SOLEDAD"
    },
    "20175016": {
        "Centro Poblado": "LA MATA"
    },
    "20175017": {
        "Centro Poblado": "EL CANAL"
    },
    "20175018": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "20175020": {
        "Centro Poblado": "PLATA PERDIDA"
    },
    "20175021": {
        "Centro Poblado": "SABANAS DE JUAN MARCOS"
    },
    "20175022": {
        "Centro Poblado": "HIGO AMARILLO"
    },
    "20175023": {
        "Centro Poblado": "BETEL"
    },
    "20175024": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "20175025": {
        "Centro Poblado": "CUATRO ESQUINAS"
    },
    "20175029": {
        "Centro Poblado": "PIEDRAS BLANCAS"
    },
    "20175030": {
        "Centro Poblado": "PUEBLITO"
    },
    "20175031": {
        "Centro Poblado": "ÚLTIMO CASO"
    },
    "20175032": {
        "Centro Poblado": "ZAPATI"
    },
    "20175033": {
        "Centro Poblado": "CABECERA"
    },
    "20175034": {
        "Centro Poblado": "CORRALITO"
    },
    "20175035": {
        "Centro Poblado": "DIOS ME VE"
    },
    "20175036": {
        "Centro Poblado": "EL PROGRESO"
    },
    "20175037": {
        "Centro Poblado": "LA INVERNA"
    },
    "20175038": {
        "Centro Poblado": "LA SABANA DEL TREBOL"
    },
    "20175039": {
        "Centro Poblado": "LA UNION"
    },
    "20175040": {
        "Centro Poblado": "MATA DE GUILLIN"
    },
    "20175041": {
        "Centro Poblado": "NUEVA VICTORIA"
    },
    "20178000": {
        "Centro Poblado": "CHIRIGUANÁ"
    },
    "20178006": {
        "Centro Poblado": "POPONTE"
    },
    "20178008": {
        "Centro Poblado": "RINCÓN HONDO"
    },
    "20178014": {
        "Centro Poblado": "LA AURORA"
    },
    "20178015": {
        "Centro Poblado": "ESTACIÓN CHIRIGUANÁ"
    },
    "20178016": {
        "Centro Poblado": "LA SIERRA"
    },
    "20178017": {
        "Centro Poblado": "AGUA FRÍA"
    },
    "20178018": {
        "Centro Poblado": "EL CRUCE DE LA SIERRA"
    },
    "20178019": {
        "Centro Poblado": "ARENAS BLANCAS"
    },
    "20178021": {
        "Centro Poblado": "CERRAJONES"
    },
    "20228000": {
        "Centro Poblado": "CURUMANÍ"
    },
    "20228001": {
        "Centro Poblado": "SABANAGRANDE"
    },
    "20228002": {
        "Centro Poblado": "SAN ROQUE"
    },
    "20228003": {
        "Centro Poblado": "SAN SEBASTIÁN"
    },
    "20228004": {
        "Centro Poblado": "SANTA ISABEL"
    },
    "20228005": {
        "Centro Poblado": "CHAMPÁN"
    },
    "20228007": {
        "Centro Poblado": "GUAIMARAL"
    },
    "20228008": {
        "Centro Poblado": "BARRIO ACOSTA"
    },
    "20228009": {
        "Centro Poblado": "HOJANCHA"
    },
    "20228011": {
        "Centro Poblado": "EL MAMEY"
    },
    "20228012": {
        "Centro Poblado": "CHINELA"
    },
    "20228014": {
        "Centro Poblado": "NUEVO HORIZONTE"
    },
    "20238000": {
        "Centro Poblado": "EL COPEY"
    },
    "20238002": {
        "Centro Poblado": "CARACOLICITO"
    },
    "20238003": {
        "Centro Poblado": "CHIMILA"
    },
    "20238004": {
        "Centro Poblado": "SAN FRANCISCO DE ASÍS"
    },
    "20250000": {
        "Centro Poblado": "EL PASO"
    },
    "20250001": {
        "Centro Poblado": "EL VALLITO"
    },
    "20250002": {
        "Centro Poblado": "LA LOMA"
    },
    "20250003": {
        "Centro Poblado": "POTRERILLO"
    },
    "20250004": {
        "Centro Poblado": "CUATRO VIENTOS"
    },
    "20250006": {
        "Centro Poblado": "EL CARMEN"
    },
    "20295000": {
        "Centro Poblado": "GAMARRA"
    },
    "20295001": {
        "Centro Poblado": "LA ESTACIÓN"
    },
    "20295002": {
        "Centro Poblado": "EL CONTENTO"
    },
    "20295004": {
        "Centro Poblado": "PALENQUILLO"
    },
    "20295005": {
        "Centro Poblado": "PUERTO MOSQUITO"
    },
    "20295006": {
        "Centro Poblado": "PUERTO VIEJO"
    },
    "20295007": {
        "Centro Poblado": "CASCAJAL"
    },
    "20310000": {
        "Centro Poblado": "GONZÁLEZ"
    },
    "20310002": {
        "Centro Poblado": "BÚRBURA"
    },
    "20310003": {
        "Centro Poblado": "CULEBRITA"
    },
    "20310006": {
        "Centro Poblado": "MONTERA"
    },
    "20310007": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "20383000": {
        "Centro Poblado": "LA GLORIA"
    },
    "20383001": {
        "Centro Poblado": "AYACUCHO"
    },
    "20383002": {
        "Centro Poblado": "CAROLINA"
    },
    "20383003": {
        "Centro Poblado": "MOLINA"
    },
    "20383005": {
        "Centro Poblado": "SIMAÑA"
    },
    "20383006": {
        "Centro Poblado": "BESOTE"
    },
    "20383010": {
        "Centro Poblado": "LA MATA"
    },
    "20383011": {
        "Centro Poblado": "ESTACIÓN FERROCARRIL"
    },
    "20383012": {
        "Centro Poblado": "LAS PUNTAS"
    },
    "20400000": {
        "Centro Poblado": "LA JAGUA DE IBIRICO"
    },
    "20400001": {
        "Centro Poblado": "LAS PALMITAS"
    },
    "20400002": {
        "Centro Poblado": "LA VICTORIA DE SAN ISIDRO"
    },
    "20400003": {
        "Centro Poblado": "BOQUERÓN"
    },
    "20443000": {
        "Centro Poblado": "MANAURE BALCÓN DEL CESAR"
    },
    "20517000": {
        "Centro Poblado": "PAILITAS"
    },
    "20517001": {
        "Centro Poblado": "LA FLORESTA"
    },
    "20517002": {
        "Centro Poblado": "RIVERA"
    },
    "20517004": {
        "Centro Poblado": "PALESTINA"
    },
    "20517006": {
        "Centro Poblado": "EL BURRO"
    },
    "20550000": {
        "Centro Poblado": "PELAYA"
    },
    "20550001": {
        "Centro Poblado": "COSTILLA"
    },
    "20550012": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "20570000": {
        "Centro Poblado": "PUEBLO BELLO"
    },
    "20570001": {
        "Centro Poblado": "LA CAJA"
    },
    "20570002": {
        "Centro Poblado": "LAS MINAS DE IRACAL"
    },
    "20570003": {
        "Centro Poblado": "NUEVO COLÓN"
    },
    "20570004": {
        "Centro Poblado": "NABUSIMAKE"
    },
    "20570005": {
        "Centro Poblado": "PALMARITO"
    },
    "20614000": {
        "Centro Poblado": "RÍO DE ORO"
    },
    "20614001": {
        "Centro Poblado": "EL MARQUÉZ"
    },
    "20614004": {
        "Centro Poblado": "LOS ANGELES"
    },
    "20614006": {
        "Centro Poblado": "MONTECITOS"
    },
    "20614010": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "20614012": {
        "Centro Poblado": "MORRISON"
    },
    "20621000": {
        "Centro Poblado": "ROBLES"
    },
    "20621001": {
        "Centro Poblado": "LOS ENCANTOS"
    },
    "20621006": {
        "Centro Poblado": "SAN JOSÉ DEL ORIENTE"
    },
    "20621011": {
        "Centro Poblado": "VARAS BLANCAS"
    },
    "20621012": {
        "Centro Poblado": "SAN JOSÉ DE ORIENTE - BETANIA"
    },
    "20621013": {
        "Centro Poblado": "MINGUILLO"
    },
    "20621015": {
        "Centro Poblado": "RABO LARGO"
    },
    "20621016": {
        "Centro Poblado": "SABANA ALTA"
    },
    "20710000": {
        "Centro Poblado": "SAN ALBERTO"
    },
    "20710001": {
        "Centro Poblado": "LA LLANA"
    },
    "20710002": {
        "Centro Poblado": "LA PALMA"
    },
    "20710005": {
        "Centro Poblado": "LÍBANO"
    },
    "20710008": {
        "Centro Poblado": "PUERTO CARREÑO"
    },
    "20750000": {
        "Centro Poblado": "SAN DIEGO"
    },
    "20750001": {
        "Centro Poblado": "LOS TUPES"
    },
    "20750002": {
        "Centro Poblado": "MEDIA LUNA"
    },
    "20750006": {
        "Centro Poblado": "EL RINCÓN"
    },
    "20750007": {
        "Centro Poblado": "LAS PITILLAS"
    },
    "20750009": {
        "Centro Poblado": "LOS BRASILES"
    },
    "20750011": {
        "Centro Poblado": "TOCAIMO"
    },
    "20750012": {
        "Centro Poblado": "NUEVAS FLORES"
    },
    "20770000": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "20770001": {
        "Centro Poblado": "AGUAS BLANCAS"
    },
    "20770003": {
        "Centro Poblado": "MINAS"
    },
    "20770004": {
        "Centro Poblado": "PUERTO OCULTO"
    },
    "20770005": {
        "Centro Poblado": "SAN JOSÉ DE LAS AMÉRICAS"
    },
    "20770006": {
        "Centro Poblado": "CANDELIA"
    },
    "20770007": {
        "Centro Poblado": "TERRAPLEN"
    },
    "20770008": {
        "Centro Poblado": "LA CURVA"
    },
    "20770009": {
        "Centro Poblado": "LA BANCA TORCOROMA"
    },
    "20770010": {
        "Centro Poblado": "CUATRO BOCAS"
    },
    "20770011": {
        "Centro Poblado": "LOS BAGRES"
    },
    "20770012": {
        "Centro Poblado": "PITA LIMÓN"
    },
    "20770016": {
        "Centro Poblado": "CAMPO AMALIA"
    },
    "20787000": {
        "Centro Poblado": "TAMALAMEQUE"
    },
    "20787001": {
        "Centro Poblado": "PALESTINA LA NUEVA"
    },
    "20787002": {
        "Centro Poblado": "LA BOCA"
    },
    "20787005": {
        "Centro Poblado": "ZAPATOSA"
    },
    "20787007": {
        "Centro Poblado": "ANTEQUERA"
    },
    "20787009": {
        "Centro Poblado": "LAS PALMAS"
    },
    "20787011": {
        "Centro Poblado": "LAS BRISAS"
    },
    "20787012": {
        "Centro Poblado": "PASACORRIENDO"
    },
    "20787013": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "20787014": {
        "Centro Poblado": "MUNDO ALREVEZ"
    },
    "20787015": {
        "Centro Poblado": "EL DOCE"
    },
    "20787016": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "20787017": {
        "Centro Poblado": "TOTUMITO"
    },
    "20787018": {
        "Centro Poblado": "MATA DE BARRO"
    },
    "23001000": {
        "Centro Poblado": "MONTERÍA"
    },
    "23001001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "23001002": {
        "Centro Poblado": "PALOTAL"
    },
    "23001003": {
        "Centro Poblado": "EL CERRITO"
    },
    "23001004": {
        "Centro Poblado": "EL SABANAL"
    },
    "23001005": {
        "Centro Poblado": "GUASIMAL"
    },
    "23001006": {
        "Centro Poblado": "JARAQUIEL"
    },
    "23001007": {
        "Centro Poblado": "LA MANTA"
    },
    "23001008": {
        "Centro Poblado": "LAS PALOMAS"
    },
    "23001009": {
        "Centro Poblado": "LETICIA - EL TRONCO"
    },
    "23001010": {
        "Centro Poblado": "LOMA VERDE"
    },
    "23001011": {
        "Centro Poblado": "LOS GARZONES"
    },
    "23001012": {
        "Centro Poblado": "NUEVO PARAÍSO"
    },
    "23001013": {
        "Centro Poblado": "NUEVA LUCÍA"
    },
    "23001014": {
        "Centro Poblado": "PATIO BONITO"
    },
    "23001015": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "23001016": {
        "Centro Poblado": "PUEBLO BUHO"
    },
    "23001017": {
        "Centro Poblado": "SAN ANTERITO"
    },
    "23001018": {
        "Centro Poblado": "SANTA CLARA"
    },
    "23001019": {
        "Centro Poblado": "SANTA ISABEL"
    },
    "23001020": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "23001021": {
        "Centro Poblado": "TRES PALMAS"
    },
    "23001022": {
        "Centro Poblado": "TRES PIEDRAS"
    },
    "23001028": {
        "Centro Poblado": "EL BARSAL"
    },
    "23001029": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23001030": {
        "Centro Poblado": "EL COCUELO"
    },
    "23001031": {
        "Centro Poblado": "MARTINICA"
    },
    "23001032": {
        "Centro Poblado": "GUATEQUE"
    },
    "23001033": {
        "Centro Poblado": "TENERIFE"
    },
    "23001034": {
        "Centro Poblado": "LA VICTORIA"
    },
    "23001035": {
        "Centro Poblado": "MORINDÓ CENTRAL"
    },
    "23001036": {
        "Centro Poblado": "BOCA DE LA CEIBA"
    },
    "23001037": {
        "Centro Poblado": "BROQUELITO"
    },
    "23001038": {
        "Centro Poblado": "EL LIMÓN"
    },
    "23001039": {
        "Centro Poblado": "EL QUINCE"
    },
    "23001040": {
        "Centro Poblado": "EL VIDRIAL"
    },
    "23001041": {
        "Centro Poblado": "ENSENADA DE LA HAMACA"
    },
    "23001042": {
        "Centro Poblado": "GALILEA"
    },
    "23001043": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "23001044": {
        "Centro Poblado": "LA FLORIDA"
    },
    "23001045": {
        "Centro Poblado": "MAQUENCAL"
    },
    "23001046": {
        "Centro Poblado": "MARACAYO"
    },
    "23001047": {
        "Centro Poblado": "MATAMOROS"
    },
    "23001048": {
        "Centro Poblado": "MOCHILAS"
    },
    "23001049": {
        "Centro Poblado": "NUEVOS HORIZONTES"
    },
    "23001050": {
        "Centro Poblado": "PALMITO PICAO"
    },
    "23001051": {
        "Centro Poblado": "PEREIRA"
    },
    "23001052": {
        "Centro Poblado": "VILLAVICENCIO"
    },
    "23001053": {
        "Centro Poblado": "YA LA LLEVA"
    },
    "23001054": {
        "Centro Poblado": "AGUA VIVAS"
    },
    "23001055": {
        "Centro Poblado": "ARENAL"
    },
    "23001059": {
        "Centro Poblado": "CALLE BARRIDA"
    },
    "23001062": {
        "Centro Poblado": "EL TAPAO"
    },
    "23001063": {
        "Centro Poblado": "LA LUCHA"
    },
    "23001064": {
        "Centro Poblado": "LA POZA"
    },
    "23001065": {
        "Centro Poblado": "LOS CEDROS"
    },
    "23001066": {
        "Centro Poblado": "LOS PANTANOS"
    },
    "23001068": {
        "Centro Poblado": "EL DOCE"
    },
    "23001069": {
        "Centro Poblado": "PUEBLO SECO"
    },
    "23001070": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "23001072": {
        "Centro Poblado": "EL FLORAL"
    },
    "23001073": {
        "Centro Poblado": "MEDELLIN - SAPO"
    },
    "23001074": {
        "Centro Poblado": "SAN JERÓNIMO (GOLERO)"
    },
    "23001075": {
        "Centro Poblado": "BESITO VOLAO"
    },
    "23001076": {
        "Centro Poblado": "COREA"
    },
    "23001077": {
        "Centro Poblado": "EL BICHO"
    },
    "23001078": {
        "Centro Poblado": "EL PORVENIR"
    },
    "23001079": {
        "Centro Poblado": "SANTA FE"
    },
    "23068000": {
        "Centro Poblado": "AYAPEL"
    },
    "23068001": {
        "Centro Poblado": "ALFONSO LÓPEZ"
    },
    "23068003": {
        "Centro Poblado": "CECILIA"
    },
    "23068004": {
        "Centro Poblado": "EL CEDRO"
    },
    "23068006": {
        "Centro Poblado": "NARIÑO"
    },
    "23068007": {
        "Centro Poblado": "PALOTAL"
    },
    "23068009": {
        "Centro Poblado": "SINCELEJITO"
    },
    "23068012": {
        "Centro Poblado": "MARRALÚ"
    },
    "23068014": {
        "Centro Poblado": "PUEBLO NUEVO - POPALES"
    },
    "23068015": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "23079000": {
        "Centro Poblado": "BUENAVISTA"
    },
    "23079001": {
        "Centro Poblado": "TIERRA SANTA"
    },
    "23079002": {
        "Centro Poblado": "VILLA FÁTIMA"
    },
    "23079003": {
        "Centro Poblado": "BELÉN"
    },
    "23079004": {
        "Centro Poblado": "NUEVA ESTACIÓN"
    },
    "23079005": {
        "Centro Poblado": "PUERTO CÓRDOBA"
    },
    "23079010": {
        "Centro Poblado": "MEJOR ESQUINA"
    },
    "23079012": {
        "Centro Poblado": "EL VIAJANO"
    },
    "23079014": {
        "Centro Poblado": "VERACRUZ"
    },
    "23079015": {
        "Centro Poblado": "SANTA CLARA"
    },
    "23079016": {
        "Centro Poblado": "SANTA FE DEL ARCIAL 1"
    },
    "23079017": {
        "Centro Poblado": "COYONPO"
    },
    "23079019": {
        "Centro Poblado": "LAS MARÍAS"
    },
    "23079020": {
        "Centro Poblado": "SANTA FE DE ARCIAL 2"
    },
    "23090000": {
        "Centro Poblado": "CANALETE"
    },
    "23090001": {
        "Centro Poblado": "EL LIMÓN"
    },
    "23090002": {
        "Centro Poblado": "POPAYÁN"
    },
    "23090007": {
        "Centro Poblado": "CADILLO"
    },
    "23090013": {
        "Centro Poblado": "EL GUINEO"
    },
    "23090020": {
        "Centro Poblado": "TIERRADENTRO"
    },
    "23090021": {
        "Centro Poblado": "QUEBRADA DE URANGO"
    },
    "23090022": {
        "Centro Poblado": "BUENOS AIRES - LAS PAVAS"
    },
    "23090023": {
        "Centro Poblado": "EL TOMATE"
    },
    "23162000": {
        "Centro Poblado": "CERETÉ"
    },
    "23162001": {
        "Centro Poblado": "MARTÍNEZ"
    },
    "23162002": {
        "Centro Poblado": "MATEO GÓMEZ"
    },
    "23162003": {
        "Centro Poblado": "RABOLARGO"
    },
    "23162004": {
        "Centro Poblado": "SEVERA"
    },
    "23162005": {
        "Centro Poblado": "CUERO CURTIDO"
    },
    "23162006": {
        "Centro Poblado": "RETIRO DE LOS INDIOS"
    },
    "23162010": {
        "Centro Poblado": "EL CHORRILLO"
    },
    "23162012": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "23162013": {
        "Centro Poblado": "EL CEDRO"
    },
    "23162014": {
        "Centro Poblado": "ZARZALITO"
    },
    "23162016": {
        "Centro Poblado": "MANGUELITO"
    },
    "23162018": {
        "Centro Poblado": "EL QUEMADO"
    },
    "23162023": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "23162025": {
        "Centro Poblado": "BUENAVISTA DEL RETIRO"
    },
    "23162026": {
        "Centro Poblado": "BUENAVISTA EL QUEMADO"
    },
    "23162027": {
        "Centro Poblado": "EL CARMEN"
    },
    "23162032": {
        "Centro Poblado": "RUSIA"
    },
    "23162033": {
        "Centro Poblado": "CAROLINA"
    },
    "23162034": {
        "Centro Poblado": "EL LÍBANO"
    },
    "23162035": {
        "Centro Poblado": "ZAPAL"
    },
    "23168000": {
        "Centro Poblado": "CHIMÁ"
    },
    "23168001": {
        "Centro Poblado": "ARACHE"
    },
    "23168002": {
        "Centro Poblado": "CAMPO BELLO"
    },
    "23168003": {
        "Centro Poblado": "CAROLINA"
    },
    "23168004": {
        "Centro Poblado": "COROZALITO"
    },
    "23168005": {
        "Centro Poblado": "PUNTA VERDE"
    },
    "23168006": {
        "Centro Poblado": "SITIO VIEJO"
    },
    "23168008": {
        "Centro Poblado": "SABANACOSTA"
    },
    "23168017": {
        "Centro Poblado": "PIMENTAL SECTOR BURRO MUERTO"
    },
    "23182000": {
        "Centro Poblado": "CHINÚ"
    },
    "23182001": {
        "Centro Poblado": "AGUAS VIVAS"
    },
    "23182002": {
        "Centro Poblado": "CACAOTAL"
    },
    "23182003": {
        "Centro Poblado": "CARBONERO"
    },
    "23182005": {
        "Centro Poblado": "HEREDIA"
    },
    "23182006": {
        "Centro Poblado": "LOS ANGELES"
    },
    "23182007": {
        "Centro Poblado": "NUEVO ORIENTE"
    },
    "23182008": {
        "Centro Poblado": "SAN MATEO"
    },
    "23182009": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "23182011": {
        "Centro Poblado": "SANTA FE"
    },
    "23182012": {
        "Centro Poblado": "SANTA ROSA"
    },
    "23182013": {
        "Centro Poblado": "FLECHAS SEVILLA"
    },
    "23182014": {
        "Centro Poblado": "TIERRA GRATA"
    },
    "23182015": {
        "Centro Poblado": "FLECHAS SABANAS"
    },
    "23182016": {
        "Centro Poblado": "GARBADO"
    },
    "23182017": {
        "Centro Poblado": "LA PANAMÁ"
    },
    "23182018": {
        "Centro Poblado": "LA PILONA"
    },
    "23182019": {
        "Centro Poblado": "RETIRO DE LOS PÉREZ"
    },
    "23182020": {
        "Centro Poblado": "ANDALUCÍA"
    },
    "23182021": {
        "Centro Poblado": "LOS ALGARROBOS"
    },
    "23182022": {
        "Centro Poblado": "EL TIGRE"
    },
    "23182024": {
        "Centro Poblado": "VILLA FÁTIMA"
    },
    "23182027": {
        "Centro Poblado": "EL DESEO"
    },
    "23182031": {
        "Centro Poblado": "PARAÍSO"
    },
    "23182033": {
        "Centro Poblado": "LAS JARABAS"
    },
    "23182035": {
        "Centro Poblado": "PAJONAL"
    },
    "23182036": {
        "Centro Poblado": "PISA BONITO"
    },
    "23182041": {
        "Centro Poblado": "LOMAS DE PIEDRA"
    },
    "23182043": {
        "Centro Poblado": "BAJO DE PIEDRA"
    },
    "23189000": {
        "Centro Poblado": "CIÉNAGA DE ORO"
    },
    "23189001": {
        "Centro Poblado": "BERÁSTEGUI"
    },
    "23189003": {
        "Centro Poblado": "LAGUNETA"
    },
    "23189004": {
        "Centro Poblado": "LOS MIMBRES"
    },
    "23189005": {
        "Centro Poblado": "PUNTA DE YÁÑEZ"
    },
    "23189007": {
        "Centro Poblado": "PUERTO DE LA CRUZ"
    },
    "23189008": {
        "Centro Poblado": "MALAGANA"
    },
    "23189013": {
        "Centro Poblado": "SUÁREZ"
    },
    "23189016": {
        "Centro Poblado": "EL SALADO"
    },
    "23189018": {
        "Centro Poblado": "LAS PIEDRAS"
    },
    "23189019": {
        "Centro Poblado": "PIJIGUAYAL"
    },
    "23189021": {
        "Centro Poblado": "SANTIAGO POBRE"
    },
    "23189023": {
        "Centro Poblado": "SAN ANTONIO DEL TÁCHIRA"
    },
    "23189024": {
        "Centro Poblado": "ROSA VIEJA"
    },
    "23189025": {
        "Centro Poblado": "LAS PALMITAS"
    },
    "23189028": {
        "Centro Poblado": "LAS BALSAS"
    },
    "23189029": {
        "Centro Poblado": "EGIPTO"
    },
    "23189030": {
        "Centro Poblado": "BARRO PRIETO"
    },
    "23189034": {
        "Centro Poblado": "LA DRAGA"
    },
    "23189044": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "23189045": {
        "Centro Poblado": "SANTIAGUITO"
    },
    "23300000": {
        "Centro Poblado": "COTORRA"
    },
    "23300003": {
        "Centro Poblado": "LOS CEDROS"
    },
    "23300006": {
        "Centro Poblado": "PASO DE LAS FLORES"
    },
    "23300007": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "23300008": {
        "Centro Poblado": "ABROJAL"
    },
    "23300010": {
        "Centro Poblado": "EL BINDE"
    },
    "23300011": {
        "Centro Poblado": "CAIMÁN"
    },
    "23300015": {
        "Centro Poblado": "LAS AREPAS"
    },
    "23300016": {
        "Centro Poblado": "TREMENTINO"
    },
    "23300020": {
        "Centro Poblado": "MORALITO"
    },
    "23300021": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "23300026": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "23300027": {
        "Centro Poblado": "SAN PABLO"
    },
    "23350000": {
        "Centro Poblado": "LA APARTADA"
    },
    "23350003": {
        "Centro Poblado": "LA BALSA"
    },
    "23350007": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "23350015": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "23350017": {
        "Centro Poblado": "PUERTO CÓRDOBA"
    },
    "23417000": {
        "Centro Poblado": "SANTA CRUZ DE LORICA"
    },
    "23417002": {
        "Centro Poblado": "EL CARITO"
    },
    "23417003": {
        "Centro Poblado": "LA DOCTRINA"
    },
    "23417004": {
        "Centro Poblado": "LAS FLORES"
    },
    "23417005": {
        "Centro Poblado": "LOS GÓMEZ"
    },
    "23417006": {
        "Centro Poblado": "LOS MONOS"
    },
    "23417007": {
        "Centro Poblado": "NARIÑO"
    },
    "23417008": {
        "Centro Poblado": "PALO DE AGUA"
    },
    "23417009": {
        "Centro Poblado": "SAN SEBASTIÁN"
    },
    "23417010": {
        "Centro Poblado": "TIERRALTA"
    },
    "23417012": {
        "Centro Poblado": "EL LAZO"
    },
    "23417014": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "23417017": {
        "Centro Poblado": "EL CAMPANO DE LOS INDIOS"
    },
    "23417018": {
        "Centro Poblado": "COTOCA ARRIBA"
    },
    "23417019": {
        "Centro Poblado": "EL RODEO"
    },
    "23417021": {
        "Centro Poblado": "REMOLINO"
    },
    "23417022": {
        "Centro Poblado": "VILLA CONCEPCION"
    },
    "23417023": {
        "Centro Poblado": "MATA DE CAÑA"
    },
    "23417024": {
        "Centro Poblado": "CASTILLERAL"
    },
    "23417025": {
        "Centro Poblado": "COTOCA ABAJO"
    },
    "23417027": {
        "Centro Poblado": "SAN NICOLÁS DE BARÍ"
    },
    "23417029": {
        "Centro Poblado": "LA SUBIDA"
    },
    "23417030": {
        "Centro Poblado": "EL PLAYÓN"
    },
    "23417031": {
        "Centro Poblado": "LA PEINADA"
    },
    "23417034": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "23417036": {
        "Centro Poblado": "LA PALMA"
    },
    "23417037": {
        "Centro Poblado": "LOS MORALES"
    },
    "23417039": {
        "Centro Poblado": "EL GUANABANO"
    },
    "23417042": {
        "Centro Poblado": "JUAN DE DIOS GARI"
    },
    "23417043": {
        "Centro Poblado": "PUEBLO CHIQUITO"
    },
    "23419000": {
        "Centro Poblado": "LOS CÓRDOBAS"
    },
    "23419002": {
        "Centro Poblado": "EL EBANO"
    },
    "23419004": {
        "Centro Poblado": "PUERTO REY"
    },
    "23419005": {
        "Centro Poblado": "SANTA ROSA LA CAÑA"
    },
    "23419010": {
        "Centro Poblado": "BUENAVISTA"
    },
    "23419011": {
        "Centro Poblado": "LA SALADA"
    },
    "23419012": {
        "Centro Poblado": "MORINDÓ SANTANA"
    },
    "23419013": {
        "Centro Poblado": "JALISCO"
    },
    "23419019": {
        "Centro Poblado": "EL GUÁIMARO"
    },
    "23419020": {
        "Centro Poblado": "LA APONDERANCIA"
    },
    "23419025": {
        "Centro Poblado": "LOS ESQUIMALES"
    },
    "23419026": {
        "Centro Poblado": "MINUTO DE DIOS"
    },
    "23419030": {
        "Centro Poblado": "NUEVO NARIÑO"
    },
    "23464000": {
        "Centro Poblado": "MOMIL"
    },
    "23464001": {
        "Centro Poblado": "SABANETA"
    },
    "23464002": {
        "Centro Poblado": "SACANA"
    },
    "23464003": {
        "Centro Poblado": "TREMENTINO"
    },
    "23464005": {
        "Centro Poblado": "PUEBLECITO"
    },
    "23464006": {
        "Centro Poblado": "GUAYMARAL"
    },
    "23464007": {
        "Centro Poblado": "BETULIA"
    },
    "23466000": {
        "Centro Poblado": "MONTELÍBANO"
    },
    "23466001": {
        "Centro Poblado": "EL ANCLAR"
    },
    "23466005": {
        "Centro Poblado": "SAN FRANCISCO DEL RAYO"
    },
    "23466006": {
        "Centro Poblado": "TIERRADENTRO"
    },
    "23466008": {
        "Centro Poblado": "PICA PICA NUEVO"
    },
    "23466021": {
        "Centro Poblado": "PUERTO ANCHICA"
    },
    "23466023": {
        "Centro Poblado": "CÓRDOBA"
    },
    "23466028": {
        "Centro Poblado": "EL PALMAR"
    },
    "23466031": {
        "Centro Poblado": "LAS MARGARITAS"
    },
    "23466033": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "23466037": {
        "Centro Poblado": "VILLA CARMINIA"
    },
    "23500000": {
        "Centro Poblado": "MOÑITOS"
    },
    "23500001": {
        "Centro Poblado": "RÍO CEDRO"
    },
    "23500002": {
        "Centro Poblado": "SANTANDER DE LA CRUZ"
    },
    "23500003": {
        "Centro Poblado": "LA UNION"
    },
    "23500004": {
        "Centro Poblado": "BAJO DEL LIMÓN"
    },
    "23500005": {
        "Centro Poblado": "BELLA COHITA"
    },
    "23500006": {
        "Centro Poblado": "BROQUELES"
    },
    "23500010": {
        "Centro Poblado": "LA RADA"
    },
    "23500011": {
        "Centro Poblado": "LAS MUJERES"
    },
    "23500016": {
        "Centro Poblado": "NARANJAL"
    },
    "23500023": {
        "Centro Poblado": "PERPETUO SOCORRO"
    },
    "23500024": {
        "Centro Poblado": "PUEBLITO"
    },
    "23500029": {
        "Centro Poblado": "SAN ANTERITO"
    },
    "23555000": {
        "Centro Poblado": "PLANETA RICA"
    },
    "23555001": {
        "Centro Poblado": "ARENOSO"
    },
    "23555002": {
        "Centro Poblado": "CAMPO BELLO"
    },
    "23555003": {
        "Centro Poblado": "CAROLINA"
    },
    "23555004": {
        "Centro Poblado": "SANTANA (CENTRO ALEGRE)"
    },
    "23555005": {
        "Centro Poblado": "EL ALMENDRO"
    },
    "23555006": {
        "Centro Poblado": "MARAÑONAL"
    },
    "23555007": {
        "Centro Poblado": "PLAZA BONITA"
    },
    "23555008": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "23555010": {
        "Centro Poblado": "MEDIO RANCHO"
    },
    "23555011": {
        "Centro Poblado": "PAMPLONA"
    },
    "23555012": {
        "Centro Poblado": "EL REPARO"
    },
    "23555013": {
        "Centro Poblado": "LOS CERROS"
    },
    "23555015": {
        "Centro Poblado": "LAS PELONAS"
    },
    "23555019": {
        "Centro Poblado": "NUEVO PARAÍSO"
    },
    "23555020": {
        "Centro Poblado": "SANTA ROSA"
    },
    "23555022": {
        "Centro Poblado": "PLANETICA"
    },
    "23555024": {
        "Centro Poblado": "ARROYO ARENA"
    },
    "23555030": {
        "Centro Poblado": "EL GUAYABO"
    },
    "23555035": {
        "Centro Poblado": "LOMA DE PIEDRA"
    },
    "23555039": {
        "Centro Poblado": "MARIMBA"
    },
    "23555044": {
        "Centro Poblado": "PUNTA VERDE"
    },
    "23555047": {
        "Centro Poblado": "SANTA ANA"
    },
    "23570000": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "23570002": {
        "Centro Poblado": "SAN JOSÉ DE CINTURA"
    },
    "23570003": {
        "Centro Poblado": "CORCOVAO"
    },
    "23570004": {
        "Centro Poblado": "EL VARAL"
    },
    "23570005": {
        "Centro Poblado": "EL POBLADO"
    },
    "23570006": {
        "Centro Poblado": "LA GRANJITA"
    },
    "23570007": {
        "Centro Poblado": "LOS LIMONES"
    },
    "23570008": {
        "Centro Poblado": "PUERTO SANTO"
    },
    "23570009": {
        "Centro Poblado": "LA MAGDALENA"
    },
    "23570011": {
        "Centro Poblado": "PALMIRA"
    },
    "23570013": {
        "Centro Poblado": "NEIVA"
    },
    "23570014": {
        "Centro Poblado": "ARROYO DE ARENAS"
    },
    "23570016": {
        "Centro Poblado": "EL CONTENTO"
    },
    "23570017": {
        "Centro Poblado": "PRIMAVERA"
    },
    "23570018": {
        "Centro Poblado": "BETANIA"
    },
    "23570020": {
        "Centro Poblado": "EL CAMPANO"
    },
    "23570021": {
        "Centro Poblado": "PUEBLO REGAO"
    },
    "23570024": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23570026": {
        "Centro Poblado": "CAFÉ PISAO"
    },
    "23570028": {
        "Centro Poblado": "LOMA DE PIEDRA"
    },
    "23570029": {
        "Centro Poblado": "APARTADA DE BETULIA"
    },
    "23570030": {
        "Centro Poblado": "EL CORRAL"
    },
    "23570031": {
        "Centro Poblado": "EL CHIPAL"
    },
    "23570032": {
        "Centro Poblado": "EL DESEO"
    },
    "23570033": {
        "Centro Poblado": "EL TOCHE"
    },
    "23570034": {
        "Centro Poblado": "VILLA ESPERANZA"
    },
    "23570035": {
        "Centro Poblado": "VENECIA"
    },
    "23574000": {
        "Centro Poblado": "PUERTO ESCONDIDO"
    },
    "23574001": {
        "Centro Poblado": "CRISTO REY"
    },
    "23574002": {
        "Centro Poblado": "EL PANTANO"
    },
    "23574003": {
        "Centro Poblado": "SAN JOSÉ DE CANALETE"
    },
    "23574004": {
        "Centro Poblado": "VILLA ESTER"
    },
    "23574005": {
        "Centro Poblado": "ARIZAL"
    },
    "23574006": {
        "Centro Poblado": "SAN LUIS"
    },
    "23574009": {
        "Centro Poblado": "LAS MUJERES"
    },
    "23574011": {
        "Centro Poblado": "EL SILENCIO"
    },
    "23574012": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "23574014": {
        "Centro Poblado": "SANTA ISABEL"
    },
    "23580000": {
        "Centro Poblado": "PUERTO LIBERTADOR"
    },
    "23580001": {
        "Centro Poblado": "LA RICA"
    },
    "23580002": {
        "Centro Poblado": "PICA PICA VIEJO"
    },
    "23580003": {
        "Centro Poblado": "VILLANUEVA"
    },
    "23580004": {
        "Centro Poblado": "JUAN JOSÉ"
    },
    "23580006": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "23580009": {
        "Centro Poblado": "SANTA FÉ DE LAS CLARAS"
    },
    "23580010": {
        "Centro Poblado": "SAN JUAN"
    },
    "23580011": {
        "Centro Poblado": "PUERTO BELÉN"
    },
    "23580012": {
        "Centro Poblado": "EL BRILLANTE"
    },
    "23580014": {
        "Centro Poblado": "PUERTO CAREPA"
    },
    "23580015": {
        "Centro Poblado": "TORNO ROJO"
    },
    "23580016": {
        "Centro Poblado": "CENTRO AMÉRICA"
    },
    "23580017": {
        "Centro Poblado": "COROSALITO"
    },
    "23580018": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23580019": {
        "Centro Poblado": "SIETE DE AGOSTO"
    },
    "23580020": {
        "Centro Poblado": "VILLA ESPERANZA"
    },
    "23586000": {
        "Centro Poblado": "PURÍSIMA DE LA CONCEPCIÓN"
    },
    "23586001": {
        "Centro Poblado": "ASERRADERO"
    },
    "23586002": {
        "Centro Poblado": "EL HUESO"
    },
    "23586003": {
        "Centro Poblado": "LOS CORRALES"
    },
    "23586004": {
        "Centro Poblado": "SAN PEDRO DE ARROYO HONDO"
    },
    "23586005": {
        "Centro Poblado": "ARENAL"
    },
    "23586006": {
        "Centro Poblado": "COMEJEN"
    },
    "23586007": {
        "Centro Poblado": "CERROPETRONA"
    },
    "23660000": {
        "Centro Poblado": "SAHAGÚN"
    },
    "23660001": {
        "Centro Poblado": "ARENAS DEL NORTE"
    },
    "23660002": {
        "Centro Poblado": "BAJO GRANDE"
    },
    "23660003": {
        "Centro Poblado": "CATALINA"
    },
    "23660004": {
        "Centro Poblado": "COLOMBOY"
    },
    "23660005": {
        "Centro Poblado": "EL CRUCERO"
    },
    "23660006": {
        "Centro Poblado": "EL VIAJANO"
    },
    "23660007": {
        "Centro Poblado": "LLANADAS"
    },
    "23660008": {
        "Centro Poblado": "LA YE"
    },
    "23660009": {
        "Centro Poblado": "MORROCOY"
    },
    "23660010": {
        "Centro Poblado": "RODANIA"
    },
    "23660011": {
        "Centro Poblado": "SALITRAL"
    },
    "23660012": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "23660013": {
        "Centro Poblado": "SANTIAGO ABAJO"
    },
    "23660014": {
        "Centro Poblado": "SABANETA"
    },
    "23660015": {
        "Centro Poblado": "AGUAS VIVAS"
    },
    "23660016": {
        "Centro Poblado": "LAS BOCAS"
    },
    "23660017": {
        "Centro Poblado": "PISA FLORES"
    },
    "23660020": {
        "Centro Poblado": "EL ROBLE"
    },
    "23660022": {
        "Centro Poblado": "EL OLIVO"
    },
    "23660023": {
        "Centro Poblado": "BRUSELAS"
    },
    "23660024": {
        "Centro Poblado": "LOS BARRILES"
    },
    "23660025": {
        "Centro Poblado": "EL REMOLINO"
    },
    "23660028": {
        "Centro Poblado": "GUAIMARITO"
    },
    "23660029": {
        "Centro Poblado": "TREMENTINO"
    },
    "23660030": {
        "Centro Poblado": "GUAIMARO"
    },
    "23660031": {
        "Centro Poblado": "LA BALSA"
    },
    "23660032": {
        "Centro Poblado": "LAS AGUADITAS"
    },
    "23660034": {
        "Centro Poblado": "SAN ANDRESITO"
    },
    "23660037": {
        "Centro Poblado": "DIVIDIVI"
    },
    "23660040": {
        "Centro Poblado": "SALGUERITO"
    },
    "23660047": {
        "Centro Poblado": "KILÓMETRO 32"
    },
    "23660048": {
        "Centro Poblado": "KILÓMETRO 34"
    },
    "23660054": {
        "Centro Poblado": "LA MUSICA"
    },
    "23660061": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "23660064": {
        "Centro Poblado": "LA QUEBRADA"
    },
    "23660066": {
        "Centro Poblado": "LOS CHIBOLOS"
    },
    "23660067": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23660068": {
        "Centro Poblado": "SABANA DE LA FUENTE"
    },
    "23670000": {
        "Centro Poblado": "SAN ANDRÉS DE SOTAVENTO"
    },
    "23670002": {
        "Centro Poblado": "CALLE LARGA"
    },
    "23670003": {
        "Centro Poblado": "EL BANCO"
    },
    "23670005": {
        "Centro Poblado": "LOS CARRETOS"
    },
    "23670009": {
        "Centro Poblado": "PUEBLECITO SUR"
    },
    "23670013": {
        "Centro Poblado": "PLAZA BONITA"
    },
    "23670014": {
        "Centro Poblado": "LAS CASITAS"
    },
    "23670015": {
        "Centro Poblado": "LOS CASTILLOS"
    },
    "23670021": {
        "Centro Poblado": "EL CONTENTO"
    },
    "23670023": {
        "Centro Poblado": "JEJÉN"
    },
    "23670025": {
        "Centro Poblado": "CRUZ DE GUAYABO"
    },
    "23670026": {
        "Centro Poblado": "EL HOYAL"
    },
    "23670028": {
        "Centro Poblado": "BERLIN"
    },
    "23670029": {
        "Centro Poblado": "GARDENIA"
    },
    "23670030": {
        "Centro Poblado": "PATIO BONITO NORTE"
    },
    "23670031": {
        "Centro Poblado": "PATIO BONITO SUR"
    },
    "23670032": {
        "Centro Poblado": "SAN GREGORIO"
    },
    "23672000": {
        "Centro Poblado": "SAN ANTERO"
    },
    "23672001": {
        "Centro Poblado": "EL PORVENIR"
    },
    "23672003": {
        "Centro Poblado": "NUEVO AGRADO"
    },
    "23672004": {
        "Centro Poblado": "SANTA ROSA DEL BÁLSAMO"
    },
    "23672005": {
        "Centro Poblado": "TIJERETAS"
    },
    "23672006": {
        "Centro Poblado": "BIJAITO"
    },
    "23672009": {
        "Centro Poblado": "CALAO"
    },
    "23672011": {
        "Centro Poblado": "CISPATA"
    },
    "23672012": {
        "Centro Poblado": "EL NARANJO"
    },
    "23672013": {
        "Centro Poblado": "EL PROGRESO"
    },
    "23672015": {
        "Centro Poblado": "GRAU"
    },
    "23672016": {
        "Centro Poblado": "LA BONGUITA"
    },
    "23672017": {
        "Centro Poblado": "LA PARRILLA"
    },
    "23672019": {
        "Centro Poblado": "LAS NUBES"
    },
    "23672020": {
        "Centro Poblado": "LETICIA"
    },
    "23672021": {
        "Centro Poblado": "PLAYA BLANCA"
    },
    "23672022": {
        "Centro Poblado": "PUNTA BOLIVAR"
    },
    "23672023": {
        "Centro Poblado": "SAN JOSE"
    },
    "23672024": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "23672025": {
        "Centro Poblado": "BERNARDO ESCOBAR"
    },
    "23672026": {
        "Centro Poblado": "MIRIAM PARDO"
    },
    "23672027": {
        "Centro Poblado": "SAN MARTÍN 1"
    },
    "23672028": {
        "Centro Poblado": "SAN MARTÍN 2"
    },
    "23672029": {
        "Centro Poblado": "NARANJO 1"
    },
    "23675000": {
        "Centro Poblado": "SAN BERNARDO DEL VIENTO"
    },
    "23675001": {
        "Centro Poblado": "JOSÉ MANUEL DE ALTAMIRA"
    },
    "23675003": {
        "Centro Poblado": "PASO NUEVO"
    },
    "23675005": {
        "Centro Poblado": "PLAYAS DEL VIENTO"
    },
    "23675007": {
        "Centro Poblado": "TREMENTINO"
    },
    "23675009": {
        "Centro Poblado": "SAN BLAS DE JUNÍN"
    },
    "23675012": {
        "Centro Poblado": "CHIQUÍ"
    },
    "23675013": {
        "Centro Poblado": "PAJONAL"
    },
    "23675014": {
        "Centro Poblado": "SAN JOSÉ DE LAS CAÑAS"
    },
    "23675015": {
        "Centro Poblado": "MIRAMAR"
    },
    "23675018": {
        "Centro Poblado": "CAMINO REAL"
    },
    "23675019": {
        "Centro Poblado": "EL CASTILLO"
    },
    "23675021": {
        "Centro Poblado": "TINAJONES"
    },
    "23675023": {
        "Centro Poblado": "EL DARIEN"
    },
    "23675024": {
        "Centro Poblado": "SANTA INÉS DE MONTERO"
    },
    "23678000": {
        "Centro Poblado": "SAN CARLOS"
    },
    "23678001": {
        "Centro Poblado": "EL CAMPANO"
    },
    "23678002": {
        "Centro Poblado": "CARRIZAL"
    },
    "23678003": {
        "Centro Poblado": "GUACHARACAL"
    },
    "23678004": {
        "Centro Poblado": "SANTA ROSA"
    },
    "23678005": {
        "Centro Poblado": "REMEDIO POBRE"
    },
    "23678006": {
        "Centro Poblado": "CABUYA"
    },
    "23678008": {
        "Centro Poblado": "CALLEMAR"
    },
    "23678009": {
        "Centro Poblado": "CIENAGUITA"
    },
    "23678010": {
        "Centro Poblado": "EL HATO"
    },
    "23678011": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "23678012": {
        "Centro Poblado": "EL CHARCO"
    },
    "23678016": {
        "Centro Poblado": "CALLE LARGA"
    },
    "23678018": {
        "Centro Poblado": "LAS TINAS"
    },
    "23678019": {
        "Centro Poblado": "LOS CAÑOS"
    },
    "23682000": {
        "Centro Poblado": "SAN JOSÉ DE URÉ"
    },
    "23682002": {
        "Centro Poblado": "BOCAS DE URÉ"
    },
    "23682003": {
        "Centro Poblado": "BRAZO IZQUIERDO"
    },
    "23682004": {
        "Centro Poblado": "PUEBLO FLECHAS"
    },
    "23682005": {
        "Centro Poblado": "LA DORADA"
    },
    "23682006": {
        "Centro Poblado": "VERSALLES"
    },
    "23682007": {
        "Centro Poblado": "VIERA ABAJO"
    },
    "23682009": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "23686000": {
        "Centro Poblado": "SAN PELAYO"
    },
    "23686001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "23686002": {
        "Centro Poblado": "CARRILLO"
    },
    "23686003": {
        "Centro Poblado": "LA MADERA"
    },
    "23686004": {
        "Centro Poblado": "LAS GUAMAS"
    },
    "23686005": {
        "Centro Poblado": "SABANA NUEVA"
    },
    "23686006": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "23686007": {
        "Centro Poblado": "VALPARAÍSO"
    },
    "23686008": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "23686009": {
        "Centro Poblado": "PELAYITO"
    },
    "23686011": {
        "Centro Poblado": "LAS LAURAS"
    },
    "23686012": {
        "Centro Poblado": "EL BONGO"
    },
    "23686018": {
        "Centro Poblado": "EL CHIQUI"
    },
    "23686020": {
        "Centro Poblado": "RETIRO"
    },
    "23686021": {
        "Centro Poblado": "EL OBLIGADO"
    },
    "23686022": {
        "Centro Poblado": "BONGAS MELLAS"
    },
    "23686025": {
        "Centro Poblado": "COROCITO"
    },
    "23686027": {
        "Centro Poblado": "EL BÁLSAMO"
    },
    "23686029": {
        "Centro Poblado": "EL COROZO"
    },
    "23686034": {
        "Centro Poblado": "MORROCOY"
    },
    "23686036": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "23807000": {
        "Centro Poblado": "TIERRALTA"
    },
    "23807002": {
        "Centro Poblado": "CARAMELO"
    },
    "23807004": {
        "Centro Poblado": "MANTAGORDAL"
    },
    "23807005": {
        "Centro Poblado": "NUEVA GRANADA"
    },
    "23807006": {
        "Centro Poblado": "EL SAIZA"
    },
    "23807007": {
        "Centro Poblado": "SANTA FE RALITO"
    },
    "23807008": {
        "Centro Poblado": "SEVERINERA"
    },
    "23807010": {
        "Centro Poblado": "VOLADOR"
    },
    "23807017": {
        "Centro Poblado": "FRASQUILLO NUEVO"
    },
    "23807019": {
        "Centro Poblado": "CARRIZOLA"
    },
    "23807020": {
        "Centro Poblado": "EL ÁGUILA - BATATA"
    },
    "23807026": {
        "Centro Poblado": "LOS MORALES"
    },
    "23807027": {
        "Centro Poblado": "SANTA MARTA"
    },
    "23807028": {
        "Centro Poblado": "VILLA PROVIDENCIA"
    },
    "23807029": {
        "Centro Poblado": "CRUCITO"
    },
    "23807032": {
        "Centro Poblado": "PUEBLO CEDRO"
    },
    "23807040": {
        "Centro Poblado": "CAMPO BELLO"
    },
    "23807041": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "23807042": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "23807043": {
        "Centro Poblado": "EL ROSARIO"
    },
    "23807044": {
        "Centro Poblado": "VIRGILIO VARGAS"
    },
    "23807045": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23815000": {
        "Centro Poblado": "TUCHÍN"
    },
    "23815001": {
        "Centro Poblado": "BARBACOAS"
    },
    "23815002": {
        "Centro Poblado": "CRUZ CHIQUITA"
    },
    "23815004": {
        "Centro Poblado": "FLECHAS"
    },
    "23815006": {
        "Centro Poblado": "MOLINA"
    },
    "23815007": {
        "Centro Poblado": "NUEVA ESTRELLA"
    },
    "23815009": {
        "Centro Poblado": "SAN JUAN DE LA CRUZ"
    },
    "23815010": {
        "Centro Poblado": "VIDALES"
    },
    "23815012": {
        "Centro Poblado": "ANDES"
    },
    "23815013": {
        "Centro Poblado": "BELÉN"
    },
    "23815014": {
        "Centro Poblado": "BELLA VISTA"
    },
    "23815015": {
        "Centro Poblado": "BOMBA"
    },
    "23815016": {
        "Centro Poblado": "CARRETAL"
    },
    "23815017": {
        "Centro Poblado": "EL CARIÑITO"
    },
    "23815018": {
        "Centro Poblado": "EL CARMEN"
    },
    "23815019": {
        "Centro Poblado": "EL CHUZO"
    },
    "23815020": {
        "Centro Poblado": "EL PORVENIR"
    },
    "23815021": {
        "Centro Poblado": "EL ROBLE"
    },
    "23815022": {
        "Centro Poblado": "GUAYACANES"
    },
    "23815023": {
        "Centro Poblado": "LOVERAN"
    },
    "23815024": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "23815025": {
        "Centro Poblado": "NUEVA VIDA"
    },
    "23815026": {
        "Centro Poblado": "SABANA NUEVA"
    },
    "23815027": {
        "Centro Poblado": "SABANAL"
    },
    "23815028": {
        "Centro Poblado": "SANTA CLARA"
    },
    "23815029": {
        "Centro Poblado": "SANTANDER"
    },
    "23815030": {
        "Centro Poblado": "TOLIMA"
    },
    "23815031": {
        "Centro Poblado": "VILLANUEVA"
    },
    "23815032": {
        "Centro Poblado": "EL BARZAL"
    },
    "23815033": {
        "Centro Poblado": "LA GRANJA"
    },
    "23815034": {
        "Centro Poblado": "SAN MARTIN"
    },
    "23815035": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "23855000": {
        "Centro Poblado": "VALENCIA"
    },
    "23855001": {
        "Centro Poblado": "RÍO NUEVO"
    },
    "23855003": {
        "Centro Poblado": "VILLANUEVA"
    },
    "23855006": {
        "Centro Poblado": "MATA DE MAÍZ"
    },
    "23855009": {
        "Centro Poblado": "EL REPOSO"
    },
    "23855014": {
        "Centro Poblado": "MIELES ABAJO"
    },
    "23855015": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "23855016": {
        "Centro Poblado": "MANZANARES"
    },
    "23855017": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "23855019": {
        "Centro Poblado": "GUADUAL CENTRAL"
    },
    "23855020": {
        "Centro Poblado": "JERICÓ"
    },
    "23855021": {
        "Centro Poblado": "LA LIBERTAD"
    },
    "23855023": {
        "Centro Poblado": "LAS NUBES"
    },
    "23855024": {
        "Centro Poblado": "CALLEJAS"
    },
    "25001000": {
        "Centro Poblado": "AGUA DE DIOS"
    },
    "25019000": {
        "Centro Poblado": "ALBÁN"
    },
    "25019001": {
        "Centro Poblado": "CHIMBE (DANUBIO)"
    },
    "25019002": {
        "Centro Poblado": "PANTANILLO"
    },
    "25019003": {
        "Centro Poblado": "LA MARÍA"
    },
    "25035000": {
        "Centro Poblado": "ANAPOIMA"
    },
    "25035001": {
        "Centro Poblado": "LA PAZ"
    },
    "25035002": {
        "Centro Poblado": "SAN ANTONIO DE ANAPOIMA"
    },
    "25035003": {
        "Centro Poblado": "PATIO BONITO"
    },
    "25040000": {
        "Centro Poblado": "ANOLAIMA"
    },
    "25040002": {
        "Centro Poblado": "LA FLORIDA"
    },
    "25040003": {
        "Centro Poblado": "REVENTONES"
    },
    "25040006": {
        "Centro Poblado": "CORRALEJAS"
    },
    "25053000": {
        "Centro Poblado": "ARBELÁEZ"
    },
    "25053003": {
        "Centro Poblado": "TISINCE"
    },
    "25086000": {
        "Centro Poblado": "BELTRÁN"
    },
    "25086001": {
        "Centro Poblado": "PAQUILÓ"
    },
    "25086002": {
        "Centro Poblado": "LA POPA"
    },
    "25086003": {
        "Centro Poblado": "PUERTO GRAMALOTAL"
    },
    "25095000": {
        "Centro Poblado": "BITUIMA"
    },
    "25095002": {
        "Centro Poblado": "BOQUERÓN DE ILÓ"
    },
    "25095003": {
        "Centro Poblado": "LA SIERRA"
    },
    "25099000": {
        "Centro Poblado": "BOJACÁ"
    },
    "25099002": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "25120000": {
        "Centro Poblado": "CABRERA"
    },
    "25123000": {
        "Centro Poblado": "CACHIPAY"
    },
    "25123001": {
        "Centro Poblado": "PEÑA NEGRA"
    },
    "25123003": {
        "Centro Poblado": "URBANIZACION TIERRA DE ENSUEÑO"
    },
    "25126000": {
        "Centro Poblado": "CAJICÁ"
    },
    "25126003": {
        "Centro Poblado": "RINCÓN SANTO"
    },
    "25126004": {
        "Centro Poblado": "RÍO GRANDE"
    },
    "25126005": {
        "Centro Poblado": "CANELON"
    },
    "25126006": {
        "Centro Poblado": "LOS SERENEOS"
    },
    "25126007": {
        "Centro Poblado": "LOS PASOS"
    },
    "25126008": {
        "Centro Poblado": "LA FLORIDA"
    },
    "25126009": {
        "Centro Poblado": "CALAHORRA"
    },
    "25126010": {
        "Centro Poblado": "AGUANICA"
    },
    "25126011": {
        "Centro Poblado": "LA PALMA"
    },
    "25126013": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "25126014": {
        "Centro Poblado": "CAMINO LOS VARGAS"
    },
    "25126015": {
        "Centro Poblado": "LOS LEÓN"
    },
    "25126016": {
        "Centro Poblado": "PRADO"
    },
    "25126017": {
        "Centro Poblado": "PABLO HERRERA"
    },
    "25126018": {
        "Centro Poblado": "SANTA INÉS"
    },
    "25126019": {
        "Centro Poblado": "BOSQUE MADERO"
    },
    "25126020": {
        "Centro Poblado": "QUINTAS DEL MOLINO"
    },
    "25126021": {
        "Centro Poblado": "VERDE VIVO"
    },
    "25126022": {
        "Centro Poblado": "VILLA DE LOS PINOS"
    },
    "25148000": {
        "Centro Poblado": "CAPARRAPÍ"
    },
    "25148001": {
        "Centro Poblado": "CAMBRAS"
    },
    "25148003": {
        "Centro Poblado": "EL DINDAL"
    },
    "25148005": {
        "Centro Poblado": "SAN PEDRO"
    },
    "25148006": {
        "Centro Poblado": "TATI"
    },
    "25148007": {
        "Centro Poblado": "CÓRDOBA"
    },
    "25148009": {
        "Centro Poblado": "SAN CARLOS"
    },
    "25148010": {
        "Centro Poblado": "CAMBULO"
    },
    "25148012": {
        "Centro Poblado": "SAN PABLO"
    },
    "25148016": {
        "Centro Poblado": "SAN RAMÓN ALTO"
    },
    "25151000": {
        "Centro Poblado": "CÁQUEZA"
    },
    "25154000": {
        "Centro Poblado": "CARMEN DE CARUPA"
    },
    "25168000": {
        "Centro Poblado": "CHAGUANÍ"
    },
    "25175000": {
        "Centro Poblado": "CHÍA"
    },
    "25175002": {
        "Centro Poblado": "SINDAMANOY I"
    },
    "25175003": {
        "Centro Poblado": "CUATRO ESQUINAS"
    },
    "25175005": {
        "Centro Poblado": "CERCA DE PIEDRA"
    },
    "25175006": {
        "Centro Poblado": "RINCON DE FAGUA"
    },
    "25175010": {
        "Centro Poblado": "CHIQUILINDA"
    },
    "25175013": {
        "Centro Poblado": "LA PAZ"
    },
    "25175019": {
        "Centro Poblado": "EL ESPEJO"
    },
    "25175020": {
        "Centro Poblado": "PUEBLO FUERTE"
    },
    "25175021": {
        "Centro Poblado": "PUENTE CACIQUE"
    },
    "25175023": {
        "Centro Poblado": "SANTA BARBARA"
    },
    "25175025": {
        "Centro Poblado": "VILLA JULIANA"
    },
    "25175026": {
        "Centro Poblado": "ENCENILLOS DE SINDAMANOY"
    },
    "25178000": {
        "Centro Poblado": "CHIPAQUE"
    },
    "25178012": {
        "Centro Poblado": "LLANO DE CHIPAQUE"
    },
    "25178013": {
        "Centro Poblado": "ABASTICOS"
    },
    "25181000": {
        "Centro Poblado": "CHOACHÍ"
    },
    "25181003": {
        "Centro Poblado": "POTRERO GRANDE"
    },
    "25183000": {
        "Centro Poblado": "CHOCONTÁ"
    },
    "25200000": {
        "Centro Poblado": "COGUA"
    },
    "25200002": {
        "Centro Poblado": "RODAMONTAL"
    },
    "25200004": {
        "Centro Poblado": "EL MORTIÑO"
    },
    "25200005": {
        "Centro Poblado": "LA PLAZUELA"
    },
    "25200006": {
        "Centro Poblado": "LA CHAPA"
    },
    "25200008": {
        "Centro Poblado": "EL CASCAJAL"
    },
    "25200009": {
        "Centro Poblado": "EL DURAZNO"
    },
    "25200010": {
        "Centro Poblado": "EL OLIVO"
    },
    "25200012": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "25200013": {
        "Centro Poblado": "EL ÁTICO - SECTOR ÁLVAREZ"
    },
    "25200014": {
        "Centro Poblado": "RINCÓN SANTO - SECTOR ZAMORA"
    },
    "25214000": {
        "Centro Poblado": "COTA"
    },
    "25224000": {
        "Centro Poblado": "CUCUNUBÁ"
    },
    "25245000": {
        "Centro Poblado": "EL COLEGIO"
    },
    "25245001": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "25245002": {
        "Centro Poblado": "LA VICTORIA"
    },
    "25245003": {
        "Centro Poblado": "PRADILLA"
    },
    "25245004": {
        "Centro Poblado": "LA PAZ"
    },
    "25258000": {
        "Centro Poblado": "EL PEÑÓN"
    },
    "25258001": {
        "Centro Poblado": "GUAYABAL DE TOLEDO"
    },
    "25258002": {
        "Centro Poblado": "TALAUTA"
    },
    "25260000": {
        "Centro Poblado": "EL ROSAL"
    },
    "25260003": {
        "Centro Poblado": "CRUZ VERDE"
    },
    "25260004": {
        "Centro Poblado": "PUENTE EL ROSAL"
    },
    "25260005": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "25269000": {
        "Centro Poblado": "FACATATIVÁ"
    },
    "25269001": {
        "Centro Poblado": "SAN RAFAEL  BAJO"
    },
    "25269007": {
        "Centro Poblado": "LOS ANDES"
    },
    "25269008": {
        "Centro Poblado": "LA YERBABUENA"
    },
    "25269009": {
        "Centro Poblado": "ALTO DE CÓRDOBA"
    },
    "25269010": {
        "Centro Poblado": "LOS ARRAYANES"
    },
    "25269012": {
        "Centro Poblado": "LOS MANZANOS"
    },
    "25269013": {
        "Centro Poblado": "PASO ANCHO"
    },
    "25269014": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "25269017": {
        "Centro Poblado": "SANTA MARTHA - LA ESPERANZA"
    },
    "25269019": {
        "Centro Poblado": "SAGRADO CORAZÓN"
    },
    "25269020": {
        "Centro Poblado": "VILLA MYRIAM"
    },
    "25269021": {
        "Centro Poblado": "LOS ROBLES"
    },
    "25269022": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "25269023": {
        "Centro Poblado": "TIERRA GRATA ALTA"
    },
    "25269024": {
        "Centro Poblado": "TIERRA GRATA (EL CRUCE)"
    },
    "25269035": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "25279000": {
        "Centro Poblado": "FÓMEQUE"
    },
    "25279001": {
        "Centro Poblado": "LA UNIÓN"
    },
    "25281000": {
        "Centro Poblado": "FOSCA"
    },
    "25281002": {
        "Centro Poblado": "SÁNAME"
    },
    "25286000": {
        "Centro Poblado": "FUNZA"
    },
    "25286006": {
        "Centro Poblado": "EL COCLI"
    },
    "25286007": {
        "Centro Poblado": "EL PAPAYO"
    },
    "25286008": {
        "Centro Poblado": "SAN ANTONIO LOS PINOS"
    },
    "25286009": {
        "Centro Poblado": "TIENDA NUEVA"
    },
    "25288000": {
        "Centro Poblado": "FÚQUENE"
    },
    "25288001": {
        "Centro Poblado": "CAPELLANÍA"
    },
    "25288003": {
        "Centro Poblado": "NUEVO FÚQUENE"
    },
    "25290000": {
        "Centro Poblado": "FUSAGASUGÁ"
    },
    "25290001": {
        "Centro Poblado": "LA AGUADITA"
    },
    "25290012": {
        "Centro Poblado": "EL TRIUNFO BOQUERON"
    },
    "25290014": {
        "Centro Poblado": "LA CASCADA"
    },
    "25290015": {
        "Centro Poblado": "RIO BLANCO - LOS PUENTES"
    },
    "25290016": {
        "Centro Poblado": "CHINAUTA"
    },
    "25290017": {
        "Centro Poblado": "LAS PIRAMIDES"
    },
    "25293000": {
        "Centro Poblado": "GACHALÁ"
    },
    "25293003": {
        "Centro Poblado": "SANTA RITA DEL RÍO NEGRO"
    },
    "25293006": {
        "Centro Poblado": "PALOMAS"
    },
    "25295000": {
        "Centro Poblado": "GACHANCIPÁ"
    },
    "25295005": {
        "Centro Poblado": "EL ROBLE SUR"
    },
    "25297000": {
        "Centro Poblado": "GACHETÁ"
    },
    "25299000": {
        "Centro Poblado": "GAMA"
    },
    "25299001": {
        "Centro Poblado": "SAN ROQUE"
    },
    "25307000": {
        "Centro Poblado": "GIRARDOT"
    },
    "25307004": {
        "Centro Poblado": "BERLÍN"
    },
    "25307005": {
        "Centro Poblado": "BARZALOSA"
    },
    "25307006": {
        "Centro Poblado": "PIAMONTE"
    },
    "25312000": {
        "Centro Poblado": "GRANADA"
    },
    "25312007": {
        "Centro Poblado": "LA VEINTIDOS"
    },
    "25312013": {
        "Centro Poblado": "SAN RAIMUNDO"
    },
    "25317000": {
        "Centro Poblado": "GUACHETÁ"
    },
    "25320000": {
        "Centro Poblado": "GUADUAS"
    },
    "25320001": {
        "Centro Poblado": "GUADUERO"
    },
    "25320002": {
        "Centro Poblado": "LA PAZ DE CALAMOIMA"
    },
    "25320003": {
        "Centro Poblado": "PUERTO BOGOTÁ"
    },
    "25320008": {
        "Centro Poblado": "ALTO DEL TRIGO"
    },
    "25320009": {
        "Centro Poblado": "LA CABAÑA"
    },
    "25322000": {
        "Centro Poblado": "GUASCA"
    },
    "25322002": {
        "Centro Poblado": "LA CABRERITA"
    },
    "25322004": {
        "Centro Poblado": "GAMBOA (EL PLACER)"
    },
    "25324000": {
        "Centro Poblado": "GUATAQUÍ"
    },
    "25324001": {
        "Centro Poblado": "EL PORVENIR"
    },
    "25324002": {
        "Centro Poblado": "LAS ISLAS"
    },
    "25326000": {
        "Centro Poblado": "GUATAVITA"
    },
    "25328000": {
        "Centro Poblado": "GUAYABAL DE SÍQUIMA"
    },
    "25328001": {
        "Centro Poblado": "ALTO DEL TRIGO"
    },
    "25335000": {
        "Centro Poblado": "GUAYABETAL"
    },
    "25335002": {
        "Centro Poblado": "MONTERREDONDO"
    },
    "25335003": {
        "Centro Poblado": "LAS MESAS"
    },
    "25335004": {
        "Centro Poblado": "LIMONCITOS"
    },
    "25335005": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "25335006": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "25335008": {
        "Centro Poblado": "LAS MESETAS"
    },
    "25339000": {
        "Centro Poblado": "GUTIÉRREZ"
    },
    "25339001": {
        "Centro Poblado": "PASCOTE"
    },
    "25339002": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "25368000": {
        "Centro Poblado": "JERUSALÉN"
    },
    "25372000": {
        "Centro Poblado": "JUNÍN"
    },
    "25372001": {
        "Centro Poblado": "CLARAVAL"
    },
    "25372002": {
        "Centro Poblado": "CHUSCALES"
    },
    "25372004": {
        "Centro Poblado": "SUEVA"
    },
    "25372006": {
        "Centro Poblado": "PUENTE LISIO"
    },
    "25372007": {
        "Centro Poblado": "RAMAL"
    },
    "25372008": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "25377000": {
        "Centro Poblado": "LA CALERA"
    },
    "25377002": {
        "Centro Poblado": "MUNDONUEVO"
    },
    "25377003": {
        "Centro Poblado": "EL SALITRE"
    },
    "25377008": {
        "Centro Poblado": "TREINTA Y SEIS"
    },
    "25377010": {
        "Centro Poblado": "ALTAMAR"
    },
    "25377011": {
        "Centro Poblado": "EL MANZANO"
    },
    "25377012": {
        "Centro Poblado": "LA AURORA ALTA"
    },
    "25377013": {
        "Centro Poblado": "LA CAPILLA"
    },
    "25377014": {
        "Centro Poblado": "MÁRQUEZ"
    },
    "25377015": {
        "Centro Poblado": "SAN CAYETANO"
    },
    "25377016": {
        "Centro Poblado": "SAN JOSÉ DEL TRIUNFO"
    },
    "25386000": {
        "Centro Poblado": "LA MESA"
    },
    "25386001": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "25386002": {
        "Centro Poblado": "SAN JAVIER"
    },
    "25386003": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "25394000": {
        "Centro Poblado": "LA PALMA"
    },
    "25398000": {
        "Centro Poblado": "LA PEÑA"
    },
    "25402000": {
        "Centro Poblado": "LA VEGA"
    },
    "25402002": {
        "Centro Poblado": "EL VINO"
    },
    "25407000": {
        "Centro Poblado": "LENGUAZAQUE"
    },
    "25426000": {
        "Centro Poblado": "MACHETÁ"
    },
    "25430000": {
        "Centro Poblado": "MADRID"
    },
    "25430001": {
        "Centro Poblado": "LA CUESTA"
    },
    "25430003": {
        "Centro Poblado": "EL CORZO"
    },
    "25430004": {
        "Centro Poblado": "PUENTE DE PIEDRA"
    },
    "25430005": {
        "Centro Poblado": "CHAUTA"
    },
    "25430006": {
        "Centro Poblado": "MOYANO"
    },
    "25436000": {
        "Centro Poblado": "MANTA"
    },
    "25438000": {
        "Centro Poblado": "MEDINA"
    },
    "25438003": {
        "Centro Poblado": "SAN PEDRO DE GUAJARAY"
    },
    "25438004": {
        "Centro Poblado": "SANTA TERESITA"
    },
    "25438005": {
        "Centro Poblado": "MESA DE LOS REYES"
    },
    "25438006": {
        "Centro Poblado": "LOS ALPES"
    },
    "25438010": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "25438011": {
        "Centro Poblado": "GAZADUJE"
    },
    "25473000": {
        "Centro Poblado": "MOSQUERA"
    },
    "25473004": {
        "Centro Poblado": "LOS PUENTES"
    },
    "25473007": {
        "Centro Poblado": "PARCELAS"
    },
    "25473008": {
        "Centro Poblado": "PENCAL"
    },
    "25473009": {
        "Centro Poblado": "QUINTAS DE SERREZUELA"
    },
    "25483000": {
        "Centro Poblado": "NARIÑO"
    },
    "25486000": {
        "Centro Poblado": "NEMOCÓN"
    },
    "25486001": {
        "Centro Poblado": "PATIO BONITO"
    },
    "25486002": {
        "Centro Poblado": "EL ORATORIO"
    },
    "25486003": {
        "Centro Poblado": "LA PUERTA"
    },
    "25486005": {
        "Centro Poblado": "CAMACHO"
    },
    "25486006": {
        "Centro Poblado": "EL PLAN"
    },
    "25488000": {
        "Centro Poblado": "NILO"
    },
    "25488001": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "25488002": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "25488003": {
        "Centro Poblado": "EL REDIL"
    },
    "25489000": {
        "Centro Poblado": "NIMAIMA"
    },
    "25489001": {
        "Centro Poblado": "TOBIA"
    },
    "25491000": {
        "Centro Poblado": "NOCAIMA"
    },
    "25491001": {
        "Centro Poblado": "TOBIA CHICA"
    },
    "25506000": {
        "Centro Poblado": "VENECIA"
    },
    "25506001": {
        "Centro Poblado": "APOSENTOS"
    },
    "25506005": {
        "Centro Poblado": "EL TRÉBOL"
    },
    "25513000": {
        "Centro Poblado": "PACHO"
    },
    "25513001": {
        "Centro Poblado": "PASUNCHA"
    },
    "25518000": {
        "Centro Poblado": "PAIME"
    },
    "25518001": {
        "Centro Poblado": "CUATRO CAMINOS"
    },
    "25518002": {
        "Centro Poblado": "TUDELA"
    },
    "25518004": {
        "Centro Poblado": "VENECIA"
    },
    "25524000": {
        "Centro Poblado": "PANDI"
    },
    "25530000": {
        "Centro Poblado": "PARATEBUENO"
    },
    "25530001": {
        "Centro Poblado": "MAYA"
    },
    "25530002": {
        "Centro Poblado": "SANTA CECILIA"
    },
    "25530003": {
        "Centro Poblado": "EL ENGAÑO"
    },
    "25530006": {
        "Centro Poblado": "EL JAPÓN"
    },
    "25530007": {
        "Centro Poblado": "CABULLARITO"
    },
    "25535000": {
        "Centro Poblado": "PASCA"
    },
    "25535002": {
        "Centro Poblado": "GUCHIPAS"
    },
    "25572000": {
        "Centro Poblado": "PUERTO SALGAR"
    },
    "25572001": {
        "Centro Poblado": "COLORADOS"
    },
    "25572003": {
        "Centro Poblado": "PUERTO LIBRE"
    },
    "25572005": {
        "Centro Poblado": "MORRO COLORADO"
    },
    "25580000": {
        "Centro Poblado": "PULÍ"
    },
    "25580002": {
        "Centro Poblado": "PALESTINA"
    },
    "25592000": {
        "Centro Poblado": "QUEBRADANEGRA"
    },
    "25592001": {
        "Centro Poblado": "LA MAGDALENA"
    },
    "25592003": {
        "Centro Poblado": "TOBIA - LA MILAGROSA"
    },
    "25594000": {
        "Centro Poblado": "QUETAME"
    },
    "25594002": {
        "Centro Poblado": "PUENTE QUETAME"
    },
    "25594003": {
        "Centro Poblado": "GUACAPATE"
    },
    "25596000": {
        "Centro Poblado": "QUIPILE"
    },
    "25596001": {
        "Centro Poblado": "LA SIERRA"
    },
    "25596002": {
        "Centro Poblado": "LA VIRGEN"
    },
    "25596003": {
        "Centro Poblado": "SANTA MARTA"
    },
    "25596004": {
        "Centro Poblado": "LA BOTICA"
    },
    "25599000": {
        "Centro Poblado": "APULO"
    },
    "25612000": {
        "Centro Poblado": "RICAURTE"
    },
    "25612001": {
        "Centro Poblado": "MANUEL SUR"
    },
    "25612002": {
        "Centro Poblado": "EL PASO"
    },
    "25612003": {
        "Centro Poblado": "EL PORTAL"
    },
    "25612004": {
        "Centro Poblado": "LAS VARAS"
    },
    "25612006": {
        "Centro Poblado": "SAN MARCOS POBLADO"
    },
    "25612007": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "25645000": {
        "Centro Poblado": "SAN ANTONIO DEL TEQUENDAMA"
    },
    "25645001": {
        "Centro Poblado": "SANTANDERCITO"
    },
    "25645011": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "25645016": {
        "Centro Poblado": "BELLAVISTA"
    },
    "25645017": {
        "Centro Poblado": "PRADILLA"
    },
    "25645018": {
        "Centro Poblado": "LOS NARANJOS"
    },
    "25645019": {
        "Centro Poblado": "VILLA PRADILLA"
    },
    "25645020": {
        "Centro Poblado": "VILLA SHYN (CASAS MOVILES)"
    },
    "25649000": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "25649003": {
        "Centro Poblado": "PORTONES"
    },
    "25653000": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "25653001": {
        "Centro Poblado": "CAMANCHA"
    },
    "25653002": {
        "Centro Poblado": "CUIBUCO"
    },
    "25653003": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "25653005": {
        "Centro Poblado": "ALBERGUE"
    },
    "25658000": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "25662000": {
        "Centro Poblado": "SAN JUAN DE RIOSECO"
    },
    "25662001": {
        "Centro Poblado": "CAMBAO"
    },
    "25662002": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "25718000": {
        "Centro Poblado": "SASAIMA"
    },
    "25718001": {
        "Centro Poblado": "SANTA INES"
    },
    "25718002": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "25736000": {
        "Centro Poblado": "SESQUILÉ"
    },
    "25736002": {
        "Centro Poblado": "LA PLAYA"
    },
    "25736003": {
        "Centro Poblado": "BOITIVA SAN ROQUE"
    },
    "25736004": {
        "Centro Poblado": "SIATOYA"
    },
    "25740000": {
        "Centro Poblado": "SIBATÉ"
    },
    "25740004": {
        "Centro Poblado": "SAN BENITO CENTRO"
    },
    "25740005": {
        "Centro Poblado": "CHACUA CENTRO"
    },
    "25740007": {
        "Centro Poblado": "PERICO SECTOR LA HONDA"
    },
    "25740008": {
        "Centro Poblado": "PERICO SECTOR LA MACARENA"
    },
    "25740010": {
        "Centro Poblado": "SAN FORTUNATO SECTOR LOS ZORROS"
    },
    "25740011": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "25740012": {
        "Centro Poblado": "LA UNIÓN SECTOR LA UNIÓN"
    },
    "25740013": {
        "Centro Poblado": "LA UNIÓN SECTOR PIE DE ALTO"
    },
    "25740014": {
        "Centro Poblado": "SAN BENITO SECTOR JAZMÍN"
    },
    "25743000": {
        "Centro Poblado": "SILVANIA"
    },
    "25743002": {
        "Centro Poblado": "AZAFRANAL"
    },
    "25743005": {
        "Centro Poblado": "SUBIA"
    },
    "25743006": {
        "Centro Poblado": "AGUA BONITA"
    },
    "25745000": {
        "Centro Poblado": "SIMIJACA"
    },
    "25745003": {
        "Centro Poblado": "EL RETÉN"
    },
    "25745005": {
        "Centro Poblado": "SANTA LUCIA"
    },
    "25754000": {
        "Centro Poblado": "SOACHA"
    },
    "25754001": {
        "Centro Poblado": "CHARQUITO"
    },
    "25754011": {
        "Centro Poblado": "CHACUA CABRERA"
    },
    "25758000": {
        "Centro Poblado": "SOPÓ"
    },
    "25758008": {
        "Centro Poblado": "HATOGRANDE"
    },
    "25758009": {
        "Centro Poblado": "GRATAMIRA"
    },
    "25758010": {
        "Centro Poblado": "MERCENARIO"
    },
    "25758011": {
        "Centro Poblado": "LA DIANA"
    },
    "25758012": {
        "Centro Poblado": "PUEBLO VIEJO SECTOR NIÑO"
    },
    "25769000": {
        "Centro Poblado": "SUBACHOQUE"
    },
    "25769002": {
        "Centro Poblado": "LA PRADERA"
    },
    "25769003": {
        "Centro Poblado": "GALDAMEZ"
    },
    "25769006": {
        "Centro Poblado": "CASCAJAL"
    },
    "25769007": {
        "Centro Poblado": "LLANITOS"
    },
    "25772000": {
        "Centro Poblado": "SUESCA"
    },
    "25772001": {
        "Centro Poblado": "HATO GRANDE"
    },
    "25772002": {
        "Centro Poblado": "SANTA ROSITA"
    },
    "25772004": {
        "Centro Poblado": "CACICAZGO"
    },
    "25777000": {
        "Centro Poblado": "SUPATÁ"
    },
    "25777001": {
        "Centro Poblado": "LA MAGOLA"
    },
    "25779000": {
        "Centro Poblado": "SUSA"
    },
    "25781000": {
        "Centro Poblado": "SUTATAUSA"
    },
    "25781002": {
        "Centro Poblado": "LAS PEÑAS"
    },
    "25781003": {
        "Centro Poblado": "CHIRCAL DE SANTA BARBARA"
    },
    "25781004": {
        "Centro Poblado": "LA QUINTA"
    },
    "25785000": {
        "Centro Poblado": "TABIO"
    },
    "25785001": {
        "Centro Poblado": "CARRÓN"
    },
    "25785002": {
        "Centro Poblado": "EL PENCIL"
    },
    "25785003": {
        "Centro Poblado": "PARCELACIÓN TERMALES"
    },
    "25785005": {
        "Centro Poblado": "CHICÚ"
    },
    "25785007": {
        "Centro Poblado": "EL BOTE"
    },
    "25785010": {
        "Centro Poblado": "TERPEL"
    },
    "25793000": {
        "Centro Poblado": "TAUSA"
    },
    "25793003": {
        "Centro Poblado": "BOQUERÓN"
    },
    "25793005": {
        "Centro Poblado": "DIVINO NIÑO"
    },
    "25797000": {
        "Centro Poblado": "TENA"
    },
    "25797001": {
        "Centro Poblado": "LA GRAN VÍA"
    },
    "25799000": {
        "Centro Poblado": "TENJO"
    },
    "25799001": {
        "Centro Poblado": "LA PUNTA"
    },
    "25799007": {
        "Centro Poblado": "PAN DE AZÚCAR"
    },
    "25799008": {
        "Centro Poblado": "EL PALMAR"
    },
    "25799009": {
        "Centro Poblado": "GRATAMIRA"
    },
    "25799010": {
        "Centro Poblado": "BARRIO LOS CATADI"
    },
    "25799011": {
        "Centro Poblado": "CASCAJERA"
    },
    "25799012": {
        "Centro Poblado": "LOS PINOS"
    },
    "25799014": {
        "Centro Poblado": "JUAICA"
    },
    "25799015": {
        "Centro Poblado": "ZOQUE"
    },
    "25805000": {
        "Centro Poblado": "TIBACUY"
    },
    "25805001": {
        "Centro Poblado": "BATEAS"
    },
    "25805002": {
        "Centro Poblado": "CUMACA"
    },
    "25807000": {
        "Centro Poblado": "TIBIRITA"
    },
    "25815000": {
        "Centro Poblado": "TOCAIMA"
    },
    "25815001": {
        "Centro Poblado": "PUBENZA"
    },
    "25815003": {
        "Centro Poblado": "LA SALADA"
    },
    "25815007": {
        "Centro Poblado": "LA COLORADA"
    },
    "25817000": {
        "Centro Poblado": "TOCANCIPÁ"
    },
    "25817001": {
        "Centro Poblado": "CHAUTA"
    },
    "25817002": {
        "Centro Poblado": "DULCINEA"
    },
    "25817003": {
        "Centro Poblado": "PELPAK"
    },
    "25817004": {
        "Centro Poblado": "SAN JAVIER"
    },
    "25817005": {
        "Centro Poblado": "TOLIMA - MILENION"
    },
    "25817006": {
        "Centro Poblado": "LA FUENTE"
    },
    "25817007": {
        "Centro Poblado": "CETINA"
    },
    "25817008": {
        "Centro Poblado": "ANTONIA SANTOS"
    },
    "25817012": {
        "Centro Poblado": "CHICALÁ"
    },
    "25817013": {
        "Centro Poblado": "LAS QUINTAS"
    },
    "25817015": {
        "Centro Poblado": "COLPAPEL"
    },
    "25817017": {
        "Centro Poblado": "SAN VICTORINO"
    },
    "25817018": {
        "Centro Poblado": "CAMINOS DE SIE"
    },
    "25817019": {
        "Centro Poblado": "CHICO NORTE"
    },
    "25817020": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "25817021": {
        "Centro Poblado": "EL PORVENIR"
    },
    "25817022": {
        "Centro Poblado": "EL DIVINO NIÑO"
    },
    "25817023": {
        "Centro Poblado": "LOS MANZANOS"
    },
    "25823000": {
        "Centro Poblado": "TOPAIPÍ"
    },
    "25823001": {
        "Centro Poblado": "SAN ANTONIO DE AGUILERA"
    },
    "25823002": {
        "Centro Poblado": "EL NARANJAL"
    },
    "25839000": {
        "Centro Poblado": "UBALÁ"
    },
    "25839002": {
        "Centro Poblado": "LAGUNA AZUL"
    },
    "25839003": {
        "Centro Poblado": "MÁMBITA"
    },
    "25839004": {
        "Centro Poblado": "SAN PEDRO DE JAGUA"
    },
    "25839005": {
        "Centro Poblado": "SANTA ROSA"
    },
    "25839006": {
        "Centro Poblado": "LA PLAYA"
    },
    "25839010": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "25841000": {
        "Centro Poblado": "UBAQUE"
    },
    "25843000": {
        "Centro Poblado": "VILLA DE SAN DIEGO DE UBATÉ"
    },
    "25843001": {
        "Centro Poblado": "GUATANCUY"
    },
    "25843005": {
        "Centro Poblado": "VOLCÁN BAJO"
    },
    "25843007": {
        "Centro Poblado": "SAN LUIS"
    },
    "25843009": {
        "Centro Poblado": "PALOGORDO"
    },
    "25843010": {
        "Centro Poblado": "CENTRO DEL LLANO"
    },
    "25843011": {
        "Centro Poblado": "TAUSAVITA BAJO"
    },
    "25843014": {
        "Centro Poblado": "TAUSAVITA ALTO"
    },
    "25845000": {
        "Centro Poblado": "UNE"
    },
    "25845002": {
        "Centro Poblado": "TIMASITA"
    },
    "25851000": {
        "Centro Poblado": "ÚTICA"
    },
    "25862000": {
        "Centro Poblado": "VERGARA"
    },
    "25862002": {
        "Centro Poblado": "GUACAMAYAS"
    },
    "25862004": {
        "Centro Poblado": "VILLA OLARTE"
    },
    "25862005": {
        "Centro Poblado": "CERINZA"
    },
    "25862006": {
        "Centro Poblado": "CORCEGA"
    },
    "25867000": {
        "Centro Poblado": "VIANÍ"
    },
    "25867001": {
        "Centro Poblado": "ALTO EL ROSARIO"
    },
    "25871000": {
        "Centro Poblado": "VILLAGÓMEZ"
    },
    "25873000": {
        "Centro Poblado": "VILLAPINZÓN"
    },
    "25873001": {
        "Centro Poblado": "SOATAMA"
    },
    "25875000": {
        "Centro Poblado": "VILLETA"
    },
    "25875001": {
        "Centro Poblado": "BAGAZAL"
    },
    "25875004": {
        "Centro Poblado": "EL PUENTE"
    },
    "25878000": {
        "Centro Poblado": "VIOTÁ"
    },
    "25878002": {
        "Centro Poblado": "SAN GABRIEL"
    },
    "25878003": {
        "Centro Poblado": "EL PIÑAL"
    },
    "25878004": {
        "Centro Poblado": "LIBERIA"
    },
    "25885000": {
        "Centro Poblado": "YACOPÍ"
    },
    "25885002": {
        "Centro Poblado": "GUADUALITO"
    },
    "25885004": {
        "Centro Poblado": "IBAMA"
    },
    "25885006": {
        "Centro Poblado": "LLANO MATEO"
    },
    "25885008": {
        "Centro Poblado": "TERÁN"
    },
    "25885009": {
        "Centro Poblado": "APOSENTOS"
    },
    "25885018": {
        "Centro Poblado": "PATEVACA"
    },
    "25885021": {
        "Centro Poblado": "EL CASTILLO"
    },
    "25898000": {
        "Centro Poblado": "ZIPACÓN"
    },
    "25898001": {
        "Centro Poblado": "EL OCASO"
    },
    "25898004": {
        "Centro Poblado": "LA CAPILLA"
    },
    "25898005": {
        "Centro Poblado": "LA ESTACIÓN"
    },
    "25898006": {
        "Centro Poblado": "CARTAGENA"
    },
    "25898007": {
        "Centro Poblado": "LA CABAÑA"
    },
    "25899000": {
        "Centro Poblado": "ZIPAQUIRÁ"
    },
    "25899001": {
        "Centro Poblado": "LA GRANJA"
    },
    "25899002": {
        "Centro Poblado": "BARANDILLAS"
    },
    "25899006": {
        "Centro Poblado": "PASOANCHO"
    },
    "25899007": {
        "Centro Poblado": "SAN JORGE PALO BAJO"
    },
    "25899008": {
        "Centro Poblado": "SAN JORGE PALO ALTO"
    },
    "25899009": {
        "Centro Poblado": "ALTO DEL ÁGUILA"
    },
    "25899010": {
        "Centro Poblado": "APOSENTOS ALTOS"
    },
    "25899011": {
        "Centro Poblado": "BOLÍVAR 83"
    },
    "25899012": {
        "Centro Poblado": "BOSQUES DE SILECIA"
    },
    "25899015": {
        "Centro Poblado": "EL RUDAL"
    },
    "25899017": {
        "Centro Poblado": "LOTEO LA PAZ - BOMBA TERPEL - LOTEO SUSAGUÁ"
    },
    "25899019": {
        "Centro Poblado": "LOTEO SANTA ISABEL"
    },
    "25899020": {
        "Centro Poblado": "PORTACHUELO"
    },
    "25899025": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "25899026": {
        "Centro Poblado": "SANTIAGO PÉREZ"
    },
    "25899028": {
        "Centro Poblado": "LA MARIELA"
    },
    "25899029": {
        "Centro Poblado": "EL CODITO"
    },
    "25899030": {
        "Centro Poblado": "EL KIOSKO LA GRANJA"
    },
    "25899031": {
        "Centro Poblado": "LA ESCUELA"
    },
    "25899034": {
        "Centro Poblado": "ARGELIA"
    },
    "25899035": {
        "Centro Poblado": "ARGELIA II"
    },
    "25899036": {
        "Centro Poblado": "ARGELIA III"
    },
    "25899037": {
        "Centro Poblado": "MALAGON"
    },
    "27001000": {
        "Centro Poblado": "SAN FRANCISCO DE QUIBDO"
    },
    "27001008": {
        "Centro Poblado": "BOCA DE TANANDÓ"
    },
    "27001011": {
        "Centro Poblado": "CALAHORRA"
    },
    "27001013": {
        "Centro Poblado": "CAMPOBONITO"
    },
    "27001015": {
        "Centro Poblado": "GUARANDÓ"
    },
    "27001016": {
        "Centro Poblado": "GUAYABAL"
    },
    "27001017": {
        "Centro Poblado": "LA TROJE"
    },
    "27001018": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "27001020": {
        "Centro Poblado": "SAN RAFAEL DE NEGUA"
    },
    "27001024": {
        "Centro Poblado": "SAN FRANCISCO DE ICHO"
    },
    "27001029": {
        "Centro Poblado": "TAGACHÍ"
    },
    "27001032": {
        "Centro Poblado": "TUTUNENDÓ"
    },
    "27001035": {
        "Centro Poblado": "GUADALUPE"
    },
    "27001038": {
        "Centro Poblado": "SANCENO"
    },
    "27001044": {
        "Centro Poblado": "BOCA DE NAURITA"
    },
    "27001047": {
        "Centro Poblado": "EL FUERTE"
    },
    "27001048": {
        "Centro Poblado": "SAN ANTONIO DE ICHO"
    },
    "27001052": {
        "Centro Poblado": "BOCA DE NEMOTÁ (NEMOTÁ)"
    },
    "27001054": {
        "Centro Poblado": "PACURITA (CABÍ)"
    },
    "27001060": {
        "Centro Poblado": "VILLA DEL ROSARIO"
    },
    "27001061": {
        "Centro Poblado": "WINANDO"
    },
    "27001063": {
        "Centro Poblado": "BARRANCO"
    },
    "27001066": {
        "Centro Poblado": "SAN JOAQUIN"
    },
    "27001067": {
        "Centro Poblado": "EL 21"
    },
    "27006000": {
        "Centro Poblado": "ACANDÍ"
    },
    "27006003": {
        "Centro Poblado": "CAPURGANÁ"
    },
    "27006005": {
        "Centro Poblado": "LA CALETA"
    },
    "27006007": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "27006008": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "27006009": {
        "Centro Poblado": "CHIGANDI"
    },
    "27006010": {
        "Centro Poblado": "SAPZURRO"
    },
    "27006016": {
        "Centro Poblado": "PEÑALOSA"
    },
    "27025000": {
        "Centro Poblado": "PIE DE PATO"
    },
    "27025003": {
        "Centro Poblado": "APARTADÓ"
    },
    "27025004": {
        "Centro Poblado": "CHACHAJÓ"
    },
    "27025006": {
        "Centro Poblado": "NAUCAS"
    },
    "27025007": {
        "Centro Poblado": "SAN FRANCISCO DE CUGUCHO"
    },
    "27025008": {
        "Centro Poblado": "SANTA CATALINA DE CATRU"
    },
    "27025011": {
        "Centro Poblado": "BATATAL"
    },
    "27025013": {
        "Centro Poblado": "CHIGORODÓ"
    },
    "27025014": {
        "Centro Poblado": "EL SALTO (BELLA LUZ)"
    },
    "27025016": {
        "Centro Poblado": "DOMINICO"
    },
    "27025017": {
        "Centro Poblado": "GEANDO"
    },
    "27025019": {
        "Centro Poblado": "LA DIVISA"
    },
    "27025020": {
        "Centro Poblado": "LA FELICIA"
    },
    "27025021": {
        "Centro Poblado": "LA LOMA"
    },
    "27025022": {
        "Centro Poblado": "PAVARANDÓ (PUREZA)"
    },
    "27025023": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "27025024": {
        "Centro Poblado": "MOJAUDÓ"
    },
    "27025027": {
        "Centro Poblado": "PUESTO INDIO"
    },
    "27025030": {
        "Centro Poblado": "AMPARRAIDA (SANTA RITA)"
    },
    "27025031": {
        "Centro Poblado": "PUERTO MARTÍNEZ"
    },
    "27025033": {
        "Centro Poblado": "MIACORA"
    },
    "27025035": {
        "Centro Poblado": "PUERTO ALEGRE"
    },
    "27025036": {
        "Centro Poblado": "PUERTO CÓRDOBA URUDO"
    },
    "27025037": {
        "Centro Poblado": "PUERTO ECHEVERRY"
    },
    "27025038": {
        "Centro Poblado": "PUERTO LIBIA"
    },
    "27025040": {
        "Centro Poblado": "BOCA DE LEÓN"
    },
    "27025041": {
        "Centro Poblado": "NUEVO PLATANARES"
    },
    "27050000": {
        "Centro Poblado": "YUTO"
    },
    "27050001": {
        "Centro Poblado": "ARENAL"
    },
    "27050002": {
        "Centro Poblado": "DOÑA JOSEFA"
    },
    "27050003": {
        "Centro Poblado": "SAMURINDÓ"
    },
    "27050005": {
        "Centro Poblado": "MOTOLDÓ"
    },
    "27050006": {
        "Centro Poblado": "SAN JOSÉ DE PURRÉ"
    },
    "27050007": {
        "Centro Poblado": "SAN MARTÍN DE PURRÉ"
    },
    "27050008": {
        "Centro Poblado": "LA MOLANA"
    },
    "27050009": {
        "Centro Poblado": "PUENTE DE TANANDÓ"
    },
    "27050010": {
        "Centro Poblado": "PUENTE DE PAIMADÓ"
    },
    "27050013": {
        "Centro Poblado": "LA TOMA"
    },
    "27050017": {
        "Centro Poblado": "REAL DE TANANDÓ (2DO)"
    },
    "27050018": {
        "Centro Poblado": "VARIANTE DE MOTOLDÓ"
    },
    "27073000": {
        "Centro Poblado": "BAGADÓ"
    },
    "27073004": {
        "Centro Poblado": "ENGRIVADÓ"
    },
    "27073005": {
        "Centro Poblado": "LA SIERRA"
    },
    "27073006": {
        "Centro Poblado": "PIEDRA HONDA"
    },
    "27073009": {
        "Centro Poblado": "EL SALTO"
    },
    "27073010": {
        "Centro Poblado": "PLAYA BONITA"
    },
    "27073011": {
        "Centro Poblado": "VIVÍCORA"
    },
    "27073012": {
        "Centro Poblado": "PESCADITO"
    },
    "27073013": {
        "Centro Poblado": "CUAJANDÓ"
    },
    "27073014": {
        "Centro Poblado": "MUCHICHI"
    },
    "27073015": {
        "Centro Poblado": "OCHOA"
    },
    "27075000": {
        "Centro Poblado": "CIUDAD MÚTIS"
    },
    "27075002": {
        "Centro Poblado": "EL VALLE"
    },
    "27075003": {
        "Centro Poblado": "HUACA"
    },
    "27075004": {
        "Centro Poblado": "HUINA"
    },
    "27075006": {
        "Centro Poblado": "MECANA"
    },
    "27075007": {
        "Centro Poblado": "NABUGÁ"
    },
    "27075009": {
        "Centro Poblado": "PLAYITA POTE"
    },
    "27077000": {
        "Centro Poblado": "PIZARRO"
    },
    "27077002": {
        "Centro Poblado": "BELÉN DE DOCAMPODO"
    },
    "27077005": {
        "Centro Poblado": "CUEVITA"
    },
    "27077006": {
        "Centro Poblado": "DOTENEDÓ"
    },
    "27077007": {
        "Centro Poblado": "HIJUÁ"
    },
    "27077008": {
        "Centro Poblado": "ORPÚA"
    },
    "27077009": {
        "Centro Poblado": "PAVASA"
    },
    "27077011": {
        "Centro Poblado": "PILIZA"
    },
    "27077012": {
        "Centro Poblado": "PLAYITA"
    },
    "27077014": {
        "Centro Poblado": "PUNTA PURRICHA"
    },
    "27077016": {
        "Centro Poblado": "SIVIRÚ"
    },
    "27077019": {
        "Centro Poblado": "VIRUDÓ"
    },
    "27077024": {
        "Centro Poblado": "VILLA MARÍA"
    },
    "27077026": {
        "Centro Poblado": "GUINEAL"
    },
    "27077029": {
        "Centro Poblado": "USARAGÁ"
    },
    "27077032": {
        "Centro Poblado": "PUERTO ABADÍA"
    },
    "27077034": {
        "Centro Poblado": "TOCASINA - DUBASA"
    },
    "27077035": {
        "Centro Poblado": "UNIÓN MISARA"
    },
    "27077036": {
        "Centro Poblado": "BELLA VISTA"
    },
    "27099000": {
        "Centro Poblado": "BELLAVISTA"
    },
    "27099001": {
        "Centro Poblado": "ALFONSO LÓPEZ"
    },
    "27099002": {
        "Centro Poblado": "LA LOMA DE BOJAYÁ"
    },
    "27099003": {
        "Centro Poblado": "ISLA DE LOS PALACIOS"
    },
    "27099004": {
        "Centro Poblado": "LA BOBA"
    },
    "27099005": {
        "Centro Poblado": "NAPIPI"
    },
    "27099006": {
        "Centro Poblado": "BOCA DE OPOGADO"
    },
    "27099008": {
        "Centro Poblado": "PUERTO CONTÓ"
    },
    "27099009": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "27099011": {
        "Centro Poblado": "VERACRUZ"
    },
    "27099012": {
        "Centro Poblado": "POGUE"
    },
    "27099013": {
        "Centro Poblado": "MESOPOTAMIA"
    },
    "27099015": {
        "Centro Poblado": "EL TIGRE"
    },
    "27099021": {
        "Centro Poblado": "CORAZÓN DE JESÚS"
    },
    "27099029": {
        "Centro Poblado": "PICHICORA"
    },
    "27099030": {
        "Centro Poblado": "PIEDRA CANDELA"
    },
    "27135000": {
        "Centro Poblado": "MANAGRÚ"
    },
    "27135001": {
        "Centro Poblado": "BOCA DE RASPADURA"
    },
    "27135003": {
        "Centro Poblado": "PUERTO PERVEL"
    },
    "27135004": {
        "Centro Poblado": "TARIDÓ"
    },
    "27135005": {
        "Centro Poblado": "GUAPANDÓ"
    },
    "27135007": {
        "Centro Poblado": "LA ISLA"
    },
    "27150000": {
        "Centro Poblado": "CURBARADÓ"
    },
    "27150002": {
        "Centro Poblado": "DOMINGODÓ"
    },
    "27150003": {
        "Centro Poblado": "LA GRANDE"
    },
    "27150004": {
        "Centro Poblado": "PUERTO LLERAS"
    },
    "27150006": {
        "Centro Poblado": "VIGIA DE CURBADÓ"
    },
    "27150007": {
        "Centro Poblado": "VILLA NUEVA DE MONTAÑO"
    },
    "27150012": {
        "Centro Poblado": "CHICAO"
    },
    "27150014": {
        "Centro Poblado": "LA MADRE"
    },
    "27160000": {
        "Centro Poblado": "CÉRTEGUI"
    },
    "27160002": {
        "Centro Poblado": "PARECITO"
    },
    "27160006": {
        "Centro Poblado": "MEMERÁ"
    },
    "27160007": {
        "Centro Poblado": "OGODÓ"
    },
    "27160008": {
        "Centro Poblado": "LA VUELTA"
    },
    "27160009": {
        "Centro Poblado": "LAS HAMACAS"
    },
    "27160010": {
        "Centro Poblado": "SAN JORGE"
    },
    "27160011": {
        "Centro Poblado": "NIPORDU"
    },
    "27205000": {
        "Centro Poblado": "CONDOTO"
    },
    "27205007": {
        "Centro Poblado": "OPOGODÓ"
    },
    "27205008": {
        "Centro Poblado": "SANTA ANA"
    },
    "27205014": {
        "Centro Poblado": "LA PLANTA"
    },
    "27205015": {
        "Centro Poblado": "ILARIA"
    },
    "27205016": {
        "Centro Poblado": "CONSUELO ANDRAPEDA"
    },
    "27205017": {
        "Centro Poblado": "EL PASO"
    },
    "27245000": {
        "Centro Poblado": "EL CARMEN DE ATRATO"
    },
    "27245004": {
        "Centro Poblado": "LA MANSA"
    },
    "27245005": {
        "Centro Poblado": "EL PORVENIR"
    },
    "27245006": {
        "Centro Poblado": "EL SIETE"
    },
    "27245008": {
        "Centro Poblado": "EL 18"
    },
    "27245010": {
        "Centro Poblado": "LA PAZ"
    },
    "27250000": {
        "Centro Poblado": "SANTA GENOVEVA DE DOCORDÓ"
    },
    "27250001": {
        "Centro Poblado": "COPOMÁ"
    },
    "27250002": {
        "Centro Poblado": "CUCURRUPÍ"
    },
    "27250003": {
        "Centro Poblado": "QUEBRADA DE TOGOROMÁ"
    },
    "27250005": {
        "Centro Poblado": "PICHIMÁ"
    },
    "27250006": {
        "Centro Poblado": "PALESTINA"
    },
    "27250010": {
        "Centro Poblado": "EL COCO"
    },
    "27250012": {
        "Centro Poblado": "QUÍCHARO"
    },
    "27250017": {
        "Centro Poblado": "LAS PEÑITAS"
    },
    "27250018": {
        "Centro Poblado": "LOS PEREA"
    },
    "27250019": {
        "Centro Poblado": "MUNGUIDÓ"
    },
    "27250020": {
        "Centro Poblado": "CHAPPIEN"
    },
    "27250021": {
        "Centro Poblado": "BURUJÓN"
    },
    "27250022": {
        "Centro Poblado": "PANGALITA"
    },
    "27250026": {
        "Centro Poblado": "PUERTO MURILLO"
    },
    "27250029": {
        "Centro Poblado": "PANGALÁ"
    },
    "27250030": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "27250031": {
        "Centro Poblado": "TAPARAL"
    },
    "27250032": {
        "Centro Poblado": "TAPARALITO"
    },
    "27250034": {
        "Centro Poblado": "TORDÓ"
    },
    "27250039": {
        "Centro Poblado": "UNIÓN VALSALITO"
    },
    "27250040": {
        "Centro Poblado": "BARRIOS UNIDOS"
    },
    "27250041": {
        "Centro Poblado": "CABECERA"
    },
    "27250042": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "27250043": {
        "Centro Poblado": "UNION GUAIMIA"
    },
    "27361000": {
        "Centro Poblado": "ISTMINA"
    },
    "27361004": {
        "Centro Poblado": "BASURU"
    },
    "27361009": {
        "Centro Poblado": "PRIMAVERA"
    },
    "27361029": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "27361032": {
        "Centro Poblado": "SURUCO SANTA MÓNICA"
    },
    "27361037": {
        "Centro Poblado": "CARMELITA"
    },
    "27361040": {
        "Centro Poblado": "GUINIGUINI"
    },
    "27361041": {
        "Centro Poblado": "JUANA MARCELA"
    },
    "27361042": {
        "Centro Poblado": "PAITO"
    },
    "27361043": {
        "Centro Poblado": "PLAYA GRANDE"
    },
    "27361044": {
        "Centro Poblado": "CHIGORODÓ (PUERTO SALAZAR)"
    },
    "27361049": {
        "Centro Poblado": "PRIMERA MOJARRA"
    },
    "27372000": {
        "Centro Poblado": "JURADÓ"
    },
    "27372004": {
        "Centro Poblado": "PUNTA ARDITA"
    },
    "27372007": {
        "Centro Poblado": "PUNTA PIÑA"
    },
    "27372009": {
        "Centro Poblado": "CUPICA"
    },
    "27413000": {
        "Centro Poblado": "LLORÓ"
    },
    "27413007": {
        "Centro Poblado": "BORAUDO"
    },
    "27413011": {
        "Centro Poblado": "VILLA CLARET"
    },
    "27413013": {
        "Centro Poblado": "BOCA DE CAPA"
    },
    "27413014": {
        "Centro Poblado": "BOCAS DE TUMUTUMBUDÓ"
    },
    "27413015": {
        "Centro Poblado": "CANCHIDO"
    },
    "27413016": {
        "Centro Poblado": "LA PLAYA"
    },
    "27413017": {
        "Centro Poblado": "PLAYA ALTA"
    },
    "27413018": {
        "Centro Poblado": "PUERTO MORENO"
    },
    "27425000": {
        "Centro Poblado": "BETÉ"
    },
    "27425001": {
        "Centro Poblado": "BOCA DE AMÉ"
    },
    "27425002": {
        "Centro Poblado": "BOCA DE BEBARÁ"
    },
    "27425003": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "27425004": {
        "Centro Poblado": "EL LLANO DE BEBARÁ"
    },
    "27425005": {
        "Centro Poblado": "EL LLANO DE BEBARAMÁ"
    },
    "27425006": {
        "Centro Poblado": "SAN ANTONIO DEL BUEY (CAMPO SANTO)"
    },
    "27425007": {
        "Centro Poblado": "SAN JOSÉ DE BUEY"
    },
    "27425008": {
        "Centro Poblado": "SAN ROQUE"
    },
    "27425009": {
        "Centro Poblado": "TANGÜÍ"
    },
    "27425010": {
        "Centro Poblado": "AGUA CLARA"
    },
    "27425011": {
        "Centro Poblado": "BAUDO GRANDE"
    },
    "27425012": {
        "Centro Poblado": "MEDIO BETE"
    },
    "27425013": {
        "Centro Poblado": "PUERTO SALAZAR"
    },
    "27425014": {
        "Centro Poblado": "PUNE"
    },
    "27430000": {
        "Centro Poblado": "PUERTO MELUK"
    },
    "27430002": {
        "Centro Poblado": "ARENAL"
    },
    "27430003": {
        "Centro Poblado": "BOCA DE BAUDOCITO"
    },
    "27430006": {
        "Centro Poblado": "CURUNDÓ LA BANCA"
    },
    "27430009": {
        "Centro Poblado": "PIE DE PEPE"
    },
    "27430010": {
        "Centro Poblado": "PUERTO ADÁN"
    },
    "27430013": {
        "Centro Poblado": "SAN MIGUEL BAUDOCITO"
    },
    "27430023": {
        "Centro Poblado": "QUERA"
    },
    "27430024": {
        "Centro Poblado": "BOCA DE PEPE"
    },
    "27430026": {
        "Centro Poblado": "UNIÓN MISARA"
    },
    "27430028": {
        "Centro Poblado": "BERRECUY"
    },
    "27430029": {
        "Centro Poblado": "BOCA DE CURUNDO"
    },
    "27430030": {
        "Centro Poblado": "CURUNDO LA LOMA"
    },
    "27430032": {
        "Centro Poblado": "PUERTO LIBIA"
    },
    "27450000": {
        "Centro Poblado": "ANDAGOYA"
    },
    "27450001": {
        "Centro Poblado": "BEBEDÓ"
    },
    "27450007": {
        "Centro Poblado": "LA RANCHA"
    },
    "27450008": {
        "Centro Poblado": "NOANAMÁ"
    },
    "27450013": {
        "Centro Poblado": "FUJIADÓ"
    },
    "27450015": {
        "Centro Poblado": "LA UNIÓN"
    },
    "27450017": {
        "Centro Poblado": "PUERTO MURILLO"
    },
    "27450020": {
        "Centro Poblado": "CHAMBACÚ"
    },
    "27491000": {
        "Centro Poblado": "NÓVITA"
    },
    "27491001": {
        "Centro Poblado": "EL CAJÓN"
    },
    "27491002": {
        "Centro Poblado": "EL TIGRE"
    },
    "27491006": {
        "Centro Poblado": "SAN LORENZO"
    },
    "27491007": {
        "Centro Poblado": "SESEGÓ"
    },
    "27491010": {
        "Centro Poblado": "EL TAMBITO"
    },
    "27491014": {
        "Centro Poblado": "SANTA ROSA"
    },
    "27491015": {
        "Centro Poblado": "LA PUENTE"
    },
    "27491016": {
        "Centro Poblado": "PINDAZA"
    },
    "27495000": {
        "Centro Poblado": "NUQUÍ"
    },
    "27495001": {
        "Centro Poblado": "ARUSÍ"
    },
    "27495002": {
        "Centro Poblado": "COQUÍ"
    },
    "27495003": {
        "Centro Poblado": "JURUBIRÁ"
    },
    "27495004": {
        "Centro Poblado": "PANGUÍ"
    },
    "27495005": {
        "Centro Poblado": "TRIBUGÁ"
    },
    "27495007": {
        "Centro Poblado": "PARTADÓ"
    },
    "27495008": {
        "Centro Poblado": "JOVI"
    },
    "27495010": {
        "Centro Poblado": "TERMALES"
    },
    "27495011": {
        "Centro Poblado": "BOCA DE JAGUA"
    },
    "27495012": {
        "Centro Poblado": "PUERTO INDIO"
    },
    "27495013": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "27495014": {
        "Centro Poblado": "EL MORRO"
    },
    "27580000": {
        "Centro Poblado": "SANTA RITA"
    },
    "27580004": {
        "Centro Poblado": "ENCHARCAZÓN"
    },
    "27580005": {
        "Centro Poblado": "SAN JOSÉ DE VIRO VIRO"
    },
    "27580006": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "27580008": {
        "Centro Poblado": "EL BUEY"
    },
    "27600000": {
        "Centro Poblado": "PAIMADÓ"
    },
    "27600001": {
        "Centro Poblado": "BOCA DE APARTADÓ"
    },
    "27600003": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "27600004": {
        "Centro Poblado": "VILLA CONTO"
    },
    "27600006": {
        "Centro Poblado": "CHIGUARANDÓ ALTO"
    },
    "27600007": {
        "Centro Poblado": "CHIVIGUIDÓ"
    },
    "27600010": {
        "Centro Poblado": "LA SOLEDAD"
    },
    "27600011": {
        "Centro Poblado": "LOMA DE LOS GAMBOA"
    },
    "27615000": {
        "Centro Poblado": "RIOSUCIO"
    },
    "27615006": {
        "Centro Poblado": "LA HONDA"
    },
    "27615022": {
        "Centro Poblado": "PERANCHITO"
    },
    "27615023": {
        "Centro Poblado": "BELÉN DE BAJIRÁ"
    },
    "27615027": {
        "Centro Poblado": "PUENTE AMÉRICA - CACARICA"
    },
    "27615030": {
        "Centro Poblado": "PEDEGUITA"
    },
    "27615032": {
        "Centro Poblado": "BRASITO"
    },
    "27615033": {
        "Centro Poblado": "BLANQUISET"
    },
    "27615037": {
        "Centro Poblado": "MACONDO"
    },
    "27615038": {
        "Centro Poblado": "NUEVO ORIENTE"
    },
    "27615039": {
        "Centro Poblado": "PLAYA ROJA"
    },
    "27615045": {
        "Centro Poblado": "7 DE AGOSTO"
    },
    "27615046": {
        "Centro Poblado": "LA PUNTA"
    },
    "27615047": {
        "Centro Poblado": "SANTA MARIA"
    },
    "27615048": {
        "Centro Poblado": "BRISAS"
    },
    "27615049": {
        "Centro Poblado": "CHINTADÓ MEDIO"
    },
    "27660000": {
        "Centro Poblado": "SAN JOSÉ DEL PALMAR"
    },
    "27660003": {
        "Centro Poblado": "SAN PEDRO INGARA"
    },
    "27660006": {
        "Centro Poblado": "LA ITALIA"
    },
    "27660016": {
        "Centro Poblado": "JUNTAS DE TAMANÁ"
    },
    "27745000": {
        "Centro Poblado": "SIPÍ"
    },
    "27745001": {
        "Centro Poblado": "CAÑAVERAL"
    },
    "27745003": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "27745009": {
        "Centro Poblado": "TANANDÓ"
    },
    "27745010": {
        "Centro Poblado": "BUENAS BRISAS"
    },
    "27745012": {
        "Centro Poblado": "LOMA DE CHUPEY"
    },
    "27745013": {
        "Centro Poblado": "MARQUEZA"
    },
    "27745014": {
        "Centro Poblado": "SANTA ROSA"
    },
    "27745015": {
        "Centro Poblado": "TEATINO"
    },
    "27787000": {
        "Centro Poblado": "TADÓ"
    },
    "27787002": {
        "Centro Poblado": "CARMELO"
    },
    "27787004": {
        "Centro Poblado": "TAPÓN"
    },
    "27787005": {
        "Centro Poblado": "GUARATO"
    },
    "27787009": {
        "Centro Poblado": "MUMBÚ"
    },
    "27787010": {
        "Centro Poblado": "PLAYA DE ORO"
    },
    "27787015": {
        "Centro Poblado": "CORCOBADO"
    },
    "27787016": {
        "Centro Poblado": "MANUNGARÁ"
    },
    "27787021": {
        "Centro Poblado": "TABOR"
    },
    "27787022": {
        "Centro Poblado": "ANGOSTURA"
    },
    "27787026": {
        "Centro Poblado": "GINGARABÁ"
    },
    "27800000": {
        "Centro Poblado": "UNGUÍA"
    },
    "27800001": {
        "Centro Poblado": "BALBOA"
    },
    "27800002": {
        "Centro Poblado": "GILGAL"
    },
    "27800003": {
        "Centro Poblado": "SANTA MARÍA DEL DARIÉN"
    },
    "27800004": {
        "Centro Poblado": "TANELA"
    },
    "27800005": {
        "Centro Poblado": "TITUMATE"
    },
    "27800007": {
        "Centro Poblado": "BETECITO"
    },
    "27800008": {
        "Centro Poblado": "MARRIAGA"
    },
    "27800011": {
        "Centro Poblado": "EL PUERTO"
    },
    "27800015": {
        "Centro Poblado": "ARQUIA"
    },
    "27810000": {
        "Centro Poblado": "ÁNIMAS"
    },
    "27810001": {
        "Centro Poblado": "EL PLAN DE RASPADURA"
    },
    "27810002": {
        "Centro Poblado": "LA YE"
    },
    "27810003": {
        "Centro Poblado": "SAN RAFAEL DEL DOS"
    },
    "27810004": {
        "Centro Poblado": "SAN PABLO ADENTRO"
    },
    "41001000": {
        "Centro Poblado": "NEIVA"
    },
    "41001001": {
        "Centro Poblado": "CAGUÁN"
    },
    "41001002": {
        "Centro Poblado": "CHAPINERO"
    },
    "41001003": {
        "Centro Poblado": "FORTALECILLAS"
    },
    "41001004": {
        "Centro Poblado": "GUACIRCO"
    },
    "41001007": {
        "Centro Poblado": "PALACIOS"
    },
    "41001008": {
        "Centro Poblado": "PEÑAS BLANCAS"
    },
    "41001011": {
        "Centro Poblado": "SAN LUIS"
    },
    "41001012": {
        "Centro Poblado": "VEGALARGA"
    },
    "41001013": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "41001014": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "41001016": {
        "Centro Poblado": "EL COLEGIO"
    },
    "41001017": {
        "Centro Poblado": "SAN ANTONIO DE ANACONIA"
    },
    "41001018": {
        "Centro Poblado": "AIPECITO"
    },
    "41001022": {
        "Centro Poblado": "EL VENADO"
    },
    "41001024": {
        "Centro Poblado": "PIEDRA MARCADA"
    },
    "41001029": {
        "Centro Poblado": "CEDRALITO"
    },
    "41001030": {
        "Centro Poblado": "LA MATA"
    },
    "41001031": {
        "Centro Poblado": "PRADERA"
    },
    "41001032": {
        "Centro Poblado": "CEDRAL"
    },
    "41001033": {
        "Centro Poblado": "LA JULIA"
    },
    "41001034": {
        "Centro Poblado": "SAN JORGE"
    },
    "41001036": {
        "Centro Poblado": "MOSCOVIA"
    },
    "41006000": {
        "Centro Poblado": "ACEVEDO"
    },
    "41006001": {
        "Centro Poblado": "SAN ADOLFO"
    },
    "41006003": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "41006005": {
        "Centro Poblado": "SAN MARCOS"
    },
    "41006011": {
        "Centro Poblado": "EL CARMEN"
    },
    "41013000": {
        "Centro Poblado": "AGRADO"
    },
    "41013001": {
        "Centro Poblado": "LA CAÑADA"
    },
    "41013003": {
        "Centro Poblado": "SAN JOSÉ DE BELÉN"
    },
    "41016000": {
        "Centro Poblado": "AIPE"
    },
    "41016001": {
        "Centro Poblado": "PRAGA"
    },
    "41016002": {
        "Centro Poblado": "SANTA RITA"
    },
    "41016003": {
        "Centro Poblado": "EL PATA"
    },
    "41016004": {
        "Centro Poblado": "CRUCE DE GUACIRCO"
    },
    "41016005": {
        "Centro Poblado": "LA CEJA - MESITAS"
    },
    "41020000": {
        "Centro Poblado": "ALGECIRAS"
    },
    "41020001": {
        "Centro Poblado": "EL PARAÍSO VIEJO"
    },
    "41020002": {
        "Centro Poblado": "LA ARCADIA"
    },
    "41020003": {
        "Centro Poblado": "EL TORO"
    },
    "41020006": {
        "Centro Poblado": "EL PARAÍSO NUEVO"
    },
    "41026000": {
        "Centro Poblado": "ALTAMIRA"
    },
    "41026004": {
        "Centro Poblado": "LLANO DE LA VIRGEN"
    },
    "41026005": {
        "Centro Poblado": "PUENTE"
    },
    "41078000": {
        "Centro Poblado": "BARAYA"
    },
    "41132000": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "41132001": {
        "Centro Poblado": "LA VEGA"
    },
    "41132002": {
        "Centro Poblado": "OTAS"
    },
    "41132003": {
        "Centro Poblado": "BAJO PIRAVANTE"
    },
    "41132004": {
        "Centro Poblado": "RÍO NEIVA"
    },
    "41132005": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "41132006": {
        "Centro Poblado": "LOS ROSALES"
    },
    "41206000": {
        "Centro Poblado": "COLOMBIA"
    },
    "41206002": {
        "Centro Poblado": "SANTANA"
    },
    "41206005": {
        "Centro Poblado": "SAN MARCOS"
    },
    "41244000": {
        "Centro Poblado": "ELÍAS"
    },
    "41244001": {
        "Centro Poblado": "EL VISO"
    },
    "41244002": {
        "Centro Poblado": "ORITOGUAZ"
    },
    "41298000": {
        "Centro Poblado": "GARZÓN"
    },
    "41298001": {
        "Centro Poblado": "EL RECREO"
    },
    "41298002": {
        "Centro Poblado": "LA JAGUA"
    },
    "41298003": {
        "Centro Poblado": "SAN ANTONIO DEL PESCADO"
    },
    "41298004": {
        "Centro Poblado": "ZULUAGA"
    },
    "41298005": {
        "Centro Poblado": "EL PARAÍSO"
    },
    "41298007": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "41298008": {
        "Centro Poblado": "EL MESÓN"
    },
    "41298012": {
        "Centro Poblado": "PLAZUELA"
    },
    "41298013": {
        "Centro Poblado": "CAGUANCITO"
    },
    "41298014": {
        "Centro Poblado": "EL DESCANSO"
    },
    "41298015": {
        "Centro Poblado": "MAJO"
    },
    "41298016": {
        "Centro Poblado": "SAN GERARDO"
    },
    "41298017": {
        "Centro Poblado": "SANTA MARTA"
    },
    "41298019": {
        "Centro Poblado": "JAGUALITO"
    },
    "41298020": {
        "Centro Poblado": "LA CABAÑA"
    },
    "41298021": {
        "Centro Poblado": "SAN LUIS"
    },
    "41306000": {
        "Centro Poblado": "GIGANTE"
    },
    "41306001": {
        "Centro Poblado": "LA CHIQUITA"
    },
    "41306002": {
        "Centro Poblado": "LA GRAN VÍA"
    },
    "41306003": {
        "Centro Poblado": "POTRERILLOS"
    },
    "41306004": {
        "Centro Poblado": "RIOLORO"
    },
    "41306006": {
        "Centro Poblado": "EL MESÓN"
    },
    "41306007": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "41306009": {
        "Centro Poblado": "VUELTAS ARRIBA"
    },
    "41306010": {
        "Centro Poblado": "SILVANIA"
    },
    "41306011": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "41306012": {
        "Centro Poblado": "EL JARDÍN"
    },
    "41306013": {
        "Centro Poblado": "LA GRAN VÍA EL PORVENIR"
    },
    "41306014": {
        "Centro Poblado": "EL RECREO"
    },
    "41306015": {
        "Centro Poblado": "LA BODEGA"
    },
    "41306016": {
        "Centro Poblado": "LA VEGA"
    },
    "41319000": {
        "Centro Poblado": "GUADALUPE"
    },
    "41319001": {
        "Centro Poblado": "RESINA"
    },
    "41319002": {
        "Centro Poblado": "MIRAFLORES"
    },
    "41319003": {
        "Centro Poblado": "LOS CAUCHOS"
    },
    "41319004": {
        "Centro Poblado": "POTRERILLOS"
    },
    "41319005": {
        "Centro Poblado": "CACHIMBAL"
    },
    "41319006": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "41319007": {
        "Centro Poblado": "SARTENEJAL"
    },
    "41349000": {
        "Centro Poblado": "HOBO"
    },
    "41357000": {
        "Centro Poblado": "ÍQUIRA"
    },
    "41357003": {
        "Centro Poblado": "RÍO NEGRO"
    },
    "41357004": {
        "Centro Poblado": "VALENCIA LA PAZ"
    },
    "41357005": {
        "Centro Poblado": "SAN LUIS"
    },
    "41357006": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "41359000": {
        "Centro Poblado": "SAN JOSÉ DE ISNOS"
    },
    "41359003": {
        "Centro Poblado": "EL SALTO DE BORDONES"
    },
    "41359006": {
        "Centro Poblado": "BAJO JUNIN"
    },
    "41359007": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "41359008": {
        "Centro Poblado": "CIÉNAGA GRANDE"
    },
    "41378000": {
        "Centro Poblado": "LA ARGENTINA"
    },
    "41378001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "41378002": {
        "Centro Poblado": "EL PENSIL"
    },
    "41396000": {
        "Centro Poblado": "LA PLATA"
    },
    "41396001": {
        "Centro Poblado": "BELÉN"
    },
    "41396002": {
        "Centro Poblado": "MONSERRATE"
    },
    "41396004": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "41396005": {
        "Centro Poblado": "VILLA LOSADA"
    },
    "41396006": {
        "Centro Poblado": "SAN VICENTE"
    },
    "41396009": {
        "Centro Poblado": "GALLEGO"
    },
    "41483000": {
        "Centro Poblado": "NÁTAGA"
    },
    "41483001": {
        "Centro Poblado": "PATIO BONITO"
    },
    "41483002": {
        "Centro Poblado": "LLANO BUCO"
    },
    "41483003": {
        "Centro Poblado": "YARUMAL"
    },
    "41503000": {
        "Centro Poblado": "OPORAPA"
    },
    "41503001": {
        "Centro Poblado": "SAN ROQUE"
    },
    "41503002": {
        "Centro Poblado": "EL CARMEN"
    },
    "41503003": {
        "Centro Poblado": "SAN CIRO"
    },
    "41503004": {
        "Centro Poblado": "PARAGUAY"
    },
    "41518000": {
        "Centro Poblado": "PAICOL"
    },
    "41518001": {
        "Centro Poblado": "LA REFORMA"
    },
    "41518002": {
        "Centro Poblado": "LAS LAJITAS"
    },
    "41524000": {
        "Centro Poblado": "PALERMO"
    },
    "41524001": {
        "Centro Poblado": "BETANIA"
    },
    "41524004": {
        "Centro Poblado": "OSPINA PÉREZ"
    },
    "41524005": {
        "Centro Poblado": "SAN JUAN"
    },
    "41524006": {
        "Centro Poblado": "EL JUNCAL"
    },
    "41524009": {
        "Centro Poblado": "AMBORCO"
    },
    "41530000": {
        "Centro Poblado": "PALESTINA"
    },
    "41548000": {
        "Centro Poblado": "PITAL"
    },
    "41548001": {
        "Centro Poblado": "EL SOCORRO"
    },
    "41548002": {
        "Centro Poblado": "MINAS"
    },
    "41551000": {
        "Centro Poblado": "PITALITO"
    },
    "41551001": {
        "Centro Poblado": "BRUSELAS"
    },
    "41551002": {
        "Centro Poblado": "GUACACAYO"
    },
    "41551003": {
        "Centro Poblado": "LA LAGUNA"
    },
    "41551005": {
        "Centro Poblado": "REGUEROS"
    },
    "41551006": {
        "Centro Poblado": "CHILLURCO (VILLAS DEL NORTE)"
    },
    "41551008": {
        "Centro Poblado": "CRIOLLO"
    },
    "41551009": {
        "Centro Poblado": "CHARGUAYACO"
    },
    "41551010": {
        "Centro Poblado": "PALMARITO"
    },
    "41551015": {
        "Centro Poblado": "LOS ARRAYANES"
    },
    "41615000": {
        "Centro Poblado": "RIVERA"
    },
    "41615001": {
        "Centro Poblado": "LA ULLOA"
    },
    "41615002": {
        "Centro Poblado": "RIVERITA"
    },
    "41615006": {
        "Centro Poblado": "RÍO FRÍO"
    },
    "41615007": {
        "Centro Poblado": "EL GUADUAL"
    },
    "41660000": {
        "Centro Poblado": "SALADOBLANCO"
    },
    "41660001": {
        "Centro Poblado": "LA CABAÑA"
    },
    "41660007": {
        "Centro Poblado": "MORELIA"
    },
    "41668000": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "41668001": {
        "Centro Poblado": "ALTO DEL OBISPO"
    },
    "41668002": {
        "Centro Poblado": "OBANDO"
    },
    "41668003": {
        "Centro Poblado": "VILLA FÁTIMA"
    },
    "41668004": {
        "Centro Poblado": "PUERTO QUINCHANA"
    },
    "41668006": {
        "Centro Poblado": "EL PALMAR"
    },
    "41668007": {
        "Centro Poblado": "PRADERA"
    },
    "41668008": {
        "Centro Poblado": "LOS CAUCHOS"
    },
    "41668009": {
        "Centro Poblado": "EL ROSARIO"
    },
    "41676000": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "41676001": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "41770000": {
        "Centro Poblado": "SUAZA"
    },
    "41770001": {
        "Centro Poblado": "GALLARDO"
    },
    "41770002": {
        "Centro Poblado": "GUAYABAL"
    },
    "41770011": {
        "Centro Poblado": "CRUCE ACEVEDO"
    },
    "41770012": {
        "Centro Poblado": "SAN JOSE"
    },
    "41791000": {
        "Centro Poblado": "TARQUI"
    },
    "41791001": {
        "Centro Poblado": "EL VERGEL"
    },
    "41791002": {
        "Centro Poblado": "MAITO"
    },
    "41791003": {
        "Centro Poblado": "QUITURO"
    },
    "41797000": {
        "Centro Poblado": "TESALIA"
    },
    "41797001": {
        "Centro Poblado": "PACARNÍ"
    },
    "41799000": {
        "Centro Poblado": "TELLO"
    },
    "41799001": {
        "Centro Poblado": "ANACLETO GARCÍA"
    },
    "41799002": {
        "Centro Poblado": "SIERRA DEL GRAMAL"
    },
    "41799003": {
        "Centro Poblado": "SAN ANDRÉS TELLO"
    },
    "41799004": {
        "Centro Poblado": "SIERRA DE LA CAÑADA"
    },
    "41801000": {
        "Centro Poblado": "TERUEL"
    },
    "41807000": {
        "Centro Poblado": "TIMANÁ"
    },
    "41807001": {
        "Centro Poblado": "NARANJAL"
    },
    "41807004": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "41807005": {
        "Centro Poblado": "MONTAÑITA"
    },
    "41807006": {
        "Centro Poblado": "QUINCHE"
    },
    "41807007": {
        "Centro Poblado": "COSANZA"
    },
    "41807009": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "41807010": {
        "Centro Poblado": "AGUAS CLARAS"
    },
    "41807011": {
        "Centro Poblado": "ALTO NARANJAL"
    },
    "41807013": {
        "Centro Poblado": "PANTANOS"
    },
    "41807014": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "41872000": {
        "Centro Poblado": "VILLAVIEJA"
    },
    "41872001": {
        "Centro Poblado": "POTOSÍ"
    },
    "41872002": {
        "Centro Poblado": "SAN ALFONSO"
    },
    "41872003": {
        "Centro Poblado": "HATO NUEVO"
    },
    "41872004": {
        "Centro Poblado": "POLONIA"
    },
    "41872005": {
        "Centro Poblado": "LA VICTORIA"
    },
    "41885000": {
        "Centro Poblado": "YAGUARÁ"
    },
    "44001000": {
        "Centro Poblado": "RIOHACHA, DISTRITO ESPECIAL, TURÍSTICO Y CULTURAL"
    },
    "44001001": {
        "Centro Poblado": "ARROYO ARENA"
    },
    "44001002": {
        "Centro Poblado": "BARBACOA"
    },
    "44001003": {
        "Centro Poblado": "CAMARONES"
    },
    "44001004": {
        "Centro Poblado": "CASCAJALITO"
    },
    "44001005": {
        "Centro Poblado": "COTOPRIX"
    },
    "44001008": {
        "Centro Poblado": "GALÁN"
    },
    "44001011": {
        "Centro Poblado": "MATITAS"
    },
    "44001012": {
        "Centro Poblado": "MONGUÍ"
    },
    "44001016": {
        "Centro Poblado": "TOMARRAZON (TREINTA)"
    },
    "44001017": {
        "Centro Poblado": "VILLA MARTIN (MACHO VALLO)"
    },
    "44001018": {
        "Centro Poblado": "LAS PALMAS"
    },
    "44001020": {
        "Centro Poblado": "CHOLES"
    },
    "44001021": {
        "Centro Poblado": "COMEJENES"
    },
    "44001022": {
        "Centro Poblado": "EL ABRA"
    },
    "44001023": {
        "Centro Poblado": "LAS CASITAS"
    },
    "44001024": {
        "Centro Poblado": "LOS MORENEROS"
    },
    "44001025": {
        "Centro Poblado": "PELECHUA"
    },
    "44001026": {
        "Centro Poblado": "PERICO"
    },
    "44001027": {
        "Centro Poblado": "TIGRERA"
    },
    "44001028": {
        "Centro Poblado": "ANAIME"
    },
    "44001031": {
        "Centro Poblado": "CERRILLO"
    },
    "44001032": {
        "Centro Poblado": "CUCURUMANA"
    },
    "44001033": {
        "Centro Poblado": "EBANAL"
    },
    "44001035": {
        "Centro Poblado": "JUAN Y MEDIO"
    },
    "44001036": {
        "Centro Poblado": "LA ARENA"
    },
    "44001040": {
        "Centro Poblado": "PUENTE BOMBA"
    },
    "44001041": {
        "Centro Poblado": "EL CARMEN"
    },
    "44001042": {
        "Centro Poblado": "LA COMPAÑIA"
    },
    "44001043": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "44001044": {
        "Centro Poblado": "VILLA COMPI"
    },
    "44001045": {
        "Centro Poblado": "MONTE HERMÓN"
    },
    "44035000": {
        "Centro Poblado": "ALBANIA"
    },
    "44035002": {
        "Centro Poblado": "WARE WAREN"
    },
    "44035003": {
        "Centro Poblado": "LOS REMEDIOS"
    },
    "44035004": {
        "Centro Poblado": "LOS RANCHOS"
    },
    "44035005": {
        "Centro Poblado": "PITURUMANA"
    },
    "44035006": {
        "Centro Poblado": "PORCIOSA"
    },
    "44078000": {
        "Centro Poblado": "BARRANCAS"
    },
    "44078001": {
        "Centro Poblado": "CARRETALITO"
    },
    "44078006": {
        "Centro Poblado": "PAPAYAL"
    },
    "44078007": {
        "Centro Poblado": "ROCHE"
    },
    "44078008": {
        "Centro Poblado": "SAN PEDRO"
    },
    "44078009": {
        "Centro Poblado": "GUAYACANAL"
    },
    "44078011": {
        "Centro Poblado": "POZO HONDO"
    },
    "44078013": {
        "Centro Poblado": "NUEVO OREGANAL"
    },
    "44078014": {
        "Centro Poblado": "PATILLA"
    },
    "44078015": {
        "Centro Poblado": "CHANCLETA"
    },
    "44078016": {
        "Centro Poblado": "LAS CASITAS"
    },
    "44090000": {
        "Centro Poblado": "DIBULLA"
    },
    "44090001": {
        "Centro Poblado": "LA PUNTA DE LOS REMEDIOS"
    },
    "44090002": {
        "Centro Poblado": "LAS FLORES"
    },
    "44090003": {
        "Centro Poblado": "MINGUEO"
    },
    "44090004": {
        "Centro Poblado": "PALOMINO"
    },
    "44090005": {
        "Centro Poblado": "CAMPANA NUEVO"
    },
    "44090006": {
        "Centro Poblado": "RÍO ANCHO"
    },
    "44090007": {
        "Centro Poblado": "CASA DE ALUMINIO"
    },
    "44090008": {
        "Centro Poblado": "RIO JEREZ"
    },
    "44090010": {
        "Centro Poblado": "SANTA RITA DE LA SIERRA"
    },
    "44098000": {
        "Centro Poblado": "DISTRACCIÓN"
    },
    "44098001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "44098002": {
        "Centro Poblado": "CHORRERAS"
    },
    "44098003": {
        "Centro Poblado": "CAIMITO (RESGUARDO)"
    },
    "44098005": {
        "Centro Poblado": "LA DUDA"
    },
    "44098007": {
        "Centro Poblado": "LA CEIBA (RESGUARDO)"
    },
    "44098008": {
        "Centro Poblado": "LOS HORNITOS"
    },
    "44098011": {
        "Centro Poblado": "POTRERITO"
    },
    "44098012": {
        "Centro Poblado": "PULGAR"
    },
    "44110000": {
        "Centro Poblado": "EL MOLINO"
    },
    "44279000": {
        "Centro Poblado": "FONSECA"
    },
    "44279002": {
        "Centro Poblado": "CONEJO"
    },
    "44279005": {
        "Centro Poblado": "EL HATICO"
    },
    "44279006": {
        "Centro Poblado": "SITIONUEVO"
    },
    "44279007": {
        "Centro Poblado": "CARDONAL"
    },
    "44279008": {
        "Centro Poblado": "BANGAÑITAS"
    },
    "44279011": {
        "Centro Poblado": "EL CONFUSO"
    },
    "44279013": {
        "Centro Poblado": "LOS ALTOS"
    },
    "44279014": {
        "Centro Poblado": "QUEBRACHAL"
    },
    "44279015": {
        "Centro Poblado": "POTRERITO"
    },
    "44279016": {
        "Centro Poblado": "GUAMACHAL"
    },
    "44279022": {
        "Centro Poblado": "LA LAGUNA"
    },
    "44279023": {
        "Centro Poblado": "LOS TORQUITOS"
    },
    "44378000": {
        "Centro Poblado": "HATONUEVO"
    },
    "44378004": {
        "Centro Poblado": "EL POZO"
    },
    "44378005": {
        "Centro Poblado": "GUAIMARITO"
    },
    "44420000": {
        "Centro Poblado": "LA JAGUA DEL PILAR"
    },
    "44420001": {
        "Centro Poblado": "EL PLAN"
    },
    "44430000": {
        "Centro Poblado": "MAICAO"
    },
    "44430002": {
        "Centro Poblado": "CARRAIPÍA"
    },
    "44430005": {
        "Centro Poblado": "LA PAZ"
    },
    "44430006": {
        "Centro Poblado": "LA MAJAYURA"
    },
    "44430007": {
        "Centro Poblado": "PARAGUACHÓN"
    },
    "44430012": {
        "Centro Poblado": "EL LIMONCITO"
    },
    "44430014": {
        "Centro Poblado": "GARRAPATERO"
    },
    "44430015": {
        "Centro Poblado": "MAKU"
    },
    "44430016": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "44430017": {
        "Centro Poblado": "SANTA ROSA"
    },
    "44430018": {
        "Centro Poblado": "DIVINO NIÑO"
    },
    "44430019": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "44430020": {
        "Centro Poblado": "MONTE LARA"
    },
    "44560000": {
        "Centro Poblado": "MANAURE"
    },
    "44560001": {
        "Centro Poblado": "ARÉMASAHIN"
    },
    "44560002": {
        "Centro Poblado": "MUSICHI"
    },
    "44560003": {
        "Centro Poblado": "EL PÁJARO"
    },
    "44560004": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "44560006": {
        "Centro Poblado": "SHIRURIA"
    },
    "44560007": {
        "Centro Poblado": "MAYAPO"
    },
    "44560008": {
        "Centro Poblado": "MANZANA"
    },
    "44560009": {
        "Centro Poblado": "LA GLORIA"
    },
    "44560010": {
        "Centro Poblado": "LA PAZ"
    },
    "44560011": {
        "Centro Poblado": "AIMARAL"
    },
    "44560012": {
        "Centro Poblado": "ARROYO LIMON"
    },
    "44560013": {
        "Centro Poblado": "POROMANA"
    },
    "44650000": {
        "Centro Poblado": "SAN JUAN DEL CESAR"
    },
    "44650001": {
        "Centro Poblado": "CAÑAVERALES"
    },
    "44650002": {
        "Centro Poblado": "CARACOLÍ"
    },
    "44650003": {
        "Centro Poblado": "CORRAL DE PIEDRA"
    },
    "44650004": {
        "Centro Poblado": "EL HATICO DE LOS INDIOS"
    },
    "44650005": {
        "Centro Poblado": "EL TABLAZO"
    },
    "44650006": {
        "Centro Poblado": "EL TOTUMO"
    },
    "44650007": {
        "Centro Poblado": "GUAYACANAL"
    },
    "44650008": {
        "Centro Poblado": "LA JUNTA"
    },
    "44650009": {
        "Centro Poblado": "LA PEÑA"
    },
    "44650010": {
        "Centro Poblado": "LA SIERRITA"
    },
    "44650011": {
        "Centro Poblado": "LOS HATICOS"
    },
    "44650012": {
        "Centro Poblado": "LOS PONDORES"
    },
    "44650013": {
        "Centro Poblado": "ZAMBRANO"
    },
    "44650014": {
        "Centro Poblado": "CORRALEJAS"
    },
    "44650016": {
        "Centro Poblado": "PONDORITOS"
    },
    "44650017": {
        "Centro Poblado": "VILLA DEL RÍO"
    },
    "44650018": {
        "Centro Poblado": "LAGUNITA"
    },
    "44650019": {
        "Centro Poblado": "LOS POZOS"
    },
    "44650021": {
        "Centro Poblado": "CURAZAO"
    },
    "44650022": {
        "Centro Poblado": "BOCA DEL MONTE"
    },
    "44650023": {
        "Centro Poblado": "LOS CARDONES"
    },
    "44650024": {
        "Centro Poblado": "EL PLACER"
    },
    "44650025": {
        "Centro Poblado": "GUAMACHAL"
    },
    "44650026": {
        "Centro Poblado": "LOS TUNALES"
    },
    "44650027": {
        "Centro Poblado": "VERACRUZ"
    },
    "44847000": {
        "Centro Poblado": "URIBIA"
    },
    "44847003": {
        "Centro Poblado": "CABO DE LA VELA"
    },
    "44847004": {
        "Centro Poblado": "CARRIZAL"
    },
    "44847007": {
        "Centro Poblado": "EL CARDÓN"
    },
    "44847012": {
        "Centro Poblado": "NAZARETH"
    },
    "44847013": {
        "Centro Poblado": "PUERTO ESTRELLA"
    },
    "44847027": {
        "Centro Poblado": "LECHIMANA"
    },
    "44847028": {
        "Centro Poblado": "MEDIA LUNA"
    },
    "44847029": {
        "Centro Poblado": "PARAISO"
    },
    "44847031": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "44847032": {
        "Centro Poblado": "SANTA ANA"
    },
    "44847033": {
        "Centro Poblado": "SANTA FE DE SIAPANA"
    },
    "44847034": {
        "Centro Poblado": "VILLA FATIMA"
    },
    "44847035": {
        "Centro Poblado": "WARPANA"
    },
    "44847036": {
        "Centro Poblado": "WARRUTAMANA"
    },
    "44847037": {
        "Centro Poblado": "WOSOSOPO"
    },
    "44847038": {
        "Centro Poblado": "YORIJARÚ"
    },
    "44855000": {
        "Centro Poblado": "URUMITA"
    },
    "44874000": {
        "Centro Poblado": "VILLANUEVA"
    },
    "47001000": {
        "Centro Poblado": "SANTA MARTA, DISTRITO TURÍSTICO, CULTURAL E HISTÓRICO"
    },
    "47001001": {
        "Centro Poblado": "BONDA"
    },
    "47001002": {
        "Centro Poblado": "CALABAZO"
    },
    "47001003": {
        "Centro Poblado": "DON DIEGO"
    },
    "47001006": {
        "Centro Poblado": "GUACHACA"
    },
    "47001009": {
        "Centro Poblado": "MINCA"
    },
    "47001010": {
        "Centro Poblado": "TAGANGA"
    },
    "47001011": {
        "Centro Poblado": "BURITACA"
    },
    "47001012": {
        "Centro Poblado": "LA QUININA"
    },
    "47001013": {
        "Centro Poblado": "TIGRERA"
    },
    "47001022": {
        "Centro Poblado": "CABAÑAS DE BURITACA"
    },
    "47001023": {
        "Centro Poblado": "CAÑAVERAL (AGUA FRÍA)"
    },
    "47001025": {
        "Centro Poblado": "CURVALITO"
    },
    "47001026": {
        "Centro Poblado": "GUACOCHE (LA LLANTA)"
    },
    "47001027": {
        "Centro Poblado": "MARKETALIA (PALOMINO)"
    },
    "47001028": {
        "Centro Poblado": "PAZ DEL CARIBE"
    },
    "47001029": {
        "Centro Poblado": "PERICO AGUAO"
    },
    "47001032": {
        "Centro Poblado": "LA REVUELTA"
    },
    "47001034": {
        "Centro Poblado": "EL TROMPITO"
    },
    "47001035": {
        "Centro Poblado": "LA AGUACATERA"
    },
    "47001036": {
        "Centro Poblado": "MACHETE PELAO"
    },
    "47001037": {
        "Centro Poblado": "NUEVO MEJICO"
    },
    "47001038": {
        "Centro Poblado": "VALLE DE GAIRA"
    },
    "47001039": {
        "Centro Poblado": "LINDEROS"
    },
    "47001040": {
        "Centro Poblado": "LOS COCOS"
    },
    "47001041": {
        "Centro Poblado": "MENDIHUACA"
    },
    "47001042": {
        "Centro Poblado": "QUEBRADA VALENCIA"
    },
    "47001043": {
        "Centro Poblado": "SAN TROPEL"
    },
    "47001044": {
        "Centro Poblado": "LOS NARANJOS"
    },
    "47001045": {
        "Centro Poblado": "NUEVO HORIZONTE (SAN RAFAEL)"
    },
    "47030000": {
        "Centro Poblado": "ALGARROBO"
    },
    "47030001": {
        "Centro Poblado": "BELLA VISTA"
    },
    "47030002": {
        "Centro Poblado": "ESTACIÓN DEL FERROCARRIL"
    },
    "47030003": {
        "Centro Poblado": "ESTACIÓN LLERAS"
    },
    "47030004": {
        "Centro Poblado": "LOMA DEL BÁLSAMO"
    },
    "47030006": {
        "Centro Poblado": "RIOMAR"
    },
    "47053000": {
        "Centro Poblado": "ARACATACA"
    },
    "47053001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "47053011": {
        "Centro Poblado": "CAUCA"
    },
    "47053013": {
        "Centro Poblado": "SAMPUÉS"
    },
    "47053016": {
        "Centro Poblado": "EL TIGRE"
    },
    "47053017": {
        "Centro Poblado": "GUNMAKÚ"
    },
    "47053018": {
        "Centro Poblado": "RIO DE PIEDRA II"
    },
    "47058000": {
        "Centro Poblado": "EL DIFICIL"
    },
    "47058001": {
        "Centro Poblado": "ALEJANDRÍA"
    },
    "47058003": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "47058005": {
        "Centro Poblado": "SAN JOSÉ DE ARIGUANÍ"
    },
    "47058008": {
        "Centro Poblado": "VADELCO"
    },
    "47058009": {
        "Centro Poblado": "CARMEN DE ARIGUANÍ"
    },
    "47161000": {
        "Centro Poblado": "CERRO DE SAN ANTONIO"
    },
    "47161002": {
        "Centro Poblado": "CANDELARIA (CAIMÁN)"
    },
    "47161003": {
        "Centro Poblado": "CONCEPCIÓN (COCO)"
    },
    "47161005": {
        "Centro Poblado": "JESÚS DEL MONTE (MICO)"
    },
    "47161006": {
        "Centro Poblado": "PUERTO NIÑO (CHARANGA)"
    },
    "47170000": {
        "Centro Poblado": "CHIVOLO"
    },
    "47170001": {
        "Centro Poblado": "LA CHINA"
    },
    "47170002": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "47170003": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "47170004": {
        "Centro Poblado": "LA POLA"
    },
    "47170005": {
        "Centro Poblado": "PLAN"
    },
    "47189000": {
        "Centro Poblado": "CIÉNAGA"
    },
    "47189004": {
        "Centro Poblado": "SAN PEDRO DE LA SIERRA"
    },
    "47189006": {
        "Centro Poblado": "SEVILLANO"
    },
    "47189018": {
        "Centro Poblado": "PALMOR"
    },
    "47189022": {
        "Centro Poblado": "CORDOBITA"
    },
    "47189023": {
        "Centro Poblado": "SIBERIA"
    },
    "47189024": {
        "Centro Poblado": "LA ISABEL"
    },
    "47189025": {
        "Centro Poblado": "MAYA"
    },
    "47189026": {
        "Centro Poblado": "SAN JAVIER"
    },
    "47205000": {
        "Centro Poblado": "CONCORDIA"
    },
    "47205001": {
        "Centro Poblado": "BÁLSAMO"
    },
    "47205002": {
        "Centro Poblado": "BELLAVISTA"
    },
    "47205003": {
        "Centro Poblado": "ROSARIO DEL CHENGUE"
    },
    "47245000": {
        "Centro Poblado": "EL BANCO"
    },
    "47245001": {
        "Centro Poblado": "AGUAESTRADA"
    },
    "47245002": {
        "Centro Poblado": "ALGARROBAL"
    },
    "47245003": {
        "Centro Poblado": "EL BARRANCO DE CHILLOA"
    },
    "47245004": {
        "Centro Poblado": "LOS NEGRITOS"
    },
    "47245005": {
        "Centro Poblado": "BELÉN"
    },
    "47245006": {
        "Centro Poblado": "CAÑO DE PALMA"
    },
    "47245007": {
        "Centro Poblado": "EL CERRITO"
    },
    "47245008": {
        "Centro Poblado": "EL TRÉBOL"
    },
    "47245010": {
        "Centro Poblado": "MENCHIQUEJO"
    },
    "47245011": {
        "Centro Poblado": "HATILLO DE LA SABANA"
    },
    "47245012": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "47245013": {
        "Centro Poblado": "SAN ROQUE"
    },
    "47245014": {
        "Centro Poblado": "TAMALAMEQUITO"
    },
    "47245016": {
        "Centro Poblado": "SAN FELIPE Y SAN EDUARDO"
    },
    "47245018": {
        "Centro Poblado": "GUACAMAYAL"
    },
    "47245019": {
        "Centro Poblado": "MALPICA"
    },
    "47245020": {
        "Centro Poblado": "GARZÓN"
    },
    "47245022": {
        "Centro Poblado": "ISLITAS"
    },
    "47245025": {
        "Centro Poblado": "BOTILLERO"
    },
    "47245028": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "47245032": {
        "Centro Poblado": "MATA DE CAÑA"
    },
    "47245033": {
        "Centro Poblado": "EL CEDRO"
    },
    "47258000": {
        "Centro Poblado": "EL PIÑÓN"
    },
    "47258001": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "47258002": {
        "Centro Poblado": "CANTAGALLAR"
    },
    "47258003": {
        "Centro Poblado": "CARRETO"
    },
    "47258004": {
        "Centro Poblado": "PLAYÓN DE OROZCO"
    },
    "47258005": {
        "Centro Poblado": "SABANAS"
    },
    "47258006": {
        "Centro Poblado": "SAN BASILIO"
    },
    "47258007": {
        "Centro Poblado": "TIO GOLLO"
    },
    "47258009": {
        "Centro Poblado": "VERANILLO"
    },
    "47258010": {
        "Centro Poblado": "LOS PATOS"
    },
    "47258011": {
        "Centro Poblado": "VÁSQUEZ"
    },
    "47258012": {
        "Centro Poblado": "LAS PALMAS"
    },
    "47258013": {
        "Centro Poblado": "LAS PAVITAS"
    },
    "47268000": {
        "Centro Poblado": "EL RETÉN"
    },
    "47268001": {
        "Centro Poblado": "SAN SEBASTIAN DEL BONGO"
    },
    "47268002": {
        "Centro Poblado": "LA COLOMBIA"
    },
    "47268003": {
        "Centro Poblado": "LAS FLORES"
    },
    "47268006": {
        "Centro Poblado": "LA POLVORITA"
    },
    "47268007": {
        "Centro Poblado": "PARATE BIEN (EL PLEITO)"
    },
    "47268008": {
        "Centro Poblado": "SAN JOSÉ DE HONDURAS"
    },
    "47268009": {
        "Centro Poblado": "LAS CABAÑITAS"
    },
    "47268010": {
        "Centro Poblado": "SALITRE"
    },
    "47288000": {
        "Centro Poblado": "FUNDACIÓN"
    },
    "47288003": {
        "Centro Poblado": "DOÑA MARÍA"
    },
    "47288004": {
        "Centro Poblado": "SANTA ROSA"
    },
    "47288013": {
        "Centro Poblado": "SANTA CLARA"
    },
    "47288014": {
        "Centro Poblado": "EL CINCUENTA"
    },
    "47288015": {
        "Centro Poblado": "EL CABRERO"
    },
    "47288016": {
        "Centro Poblado": "LA CRISTALINA"
    },
    "47288017": {
        "Centro Poblado": "SACRAMENTO"
    },
    "47318000": {
        "Centro Poblado": "GUAMAL"
    },
    "47318001": {
        "Centro Poblado": "CASA DE TABLA"
    },
    "47318002": {
        "Centro Poblado": "GUAIMARAL"
    },
    "47318003": {
        "Centro Poblado": "HATO VIEJO"
    },
    "47318004": {
        "Centro Poblado": "PEDREGOSA"
    },
    "47318005": {
        "Centro Poblado": "LOS ANDES"
    },
    "47318006": {
        "Centro Poblado": "MURILLO"
    },
    "47318008": {
        "Centro Poblado": "RICAURTE"
    },
    "47318009": {
        "Centro Poblado": "SALVADORA"
    },
    "47318010": {
        "Centro Poblado": "HURQUIJO"
    },
    "47318011": {
        "Centro Poblado": "PLAYAS BLANCAS"
    },
    "47318012": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "47318013": {
        "Centro Poblado": "CARRETERO"
    },
    "47318014": {
        "Centro Poblado": "BELLAVISTA"
    },
    "47318016": {
        "Centro Poblado": "SANTA TERESITA"
    },
    "47318017": {
        "Centro Poblado": "SAN PEDRO"
    },
    "47318018": {
        "Centro Poblado": "LAS FLORES"
    },
    "47318019": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "47318020": {
        "Centro Poblado": "LA CEIBA"
    },
    "47318023": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "47318024": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "47318025": {
        "Centro Poblado": "EL VEINTIOCHO"
    },
    "47460000": {
        "Centro Poblado": "GRANADA"
    },
    "47460001": {
        "Centro Poblado": "EL BAJO"
    },
    "47460002": {
        "Centro Poblado": "LA GLORIA"
    },
    "47460003": {
        "Centro Poblado": "LAS TINAS"
    },
    "47460004": {
        "Centro Poblado": "LOS ANDES"
    },
    "47460006": {
        "Centro Poblado": "SAN JOSÉ DE BALLESTERO"
    },
    "47460007": {
        "Centro Poblado": "EL CORRAL"
    },
    "47460008": {
        "Centro Poblado": "EL PALMAR (EL CHUZO)"
    },
    "47541000": {
        "Centro Poblado": "PEDRAZA"
    },
    "47541001": {
        "Centro Poblado": "BAHÍA HONDA"
    },
    "47541003": {
        "Centro Poblado": "BOMBA"
    },
    "47541007": {
        "Centro Poblado": "GUAQUIRÍ"
    },
    "47541008": {
        "Centro Poblado": "HEREDIA"
    },
    "47545000": {
        "Centro Poblado": "PIJIÑO"
    },
    "47545001": {
        "Centro Poblado": "CABRERA"
    },
    "47545002": {
        "Centro Poblado": "FILADELFIA"
    },
    "47545003": {
        "Centro Poblado": "SAN JOSÉ DE PREVENCIÓN"
    },
    "47545004": {
        "Centro Poblado": "CASA BLANCA"
    },
    "47545005": {
        "Centro Poblado": "LA LUCHA"
    },
    "47545007": {
        "Centro Poblado": "EL DIVIDIVI"
    },
    "47545008": {
        "Centro Poblado": "EL BRILLANTE"
    },
    "47551000": {
        "Centro Poblado": "PIVIJAY"
    },
    "47551001": {
        "Centro Poblado": "LA AVIANCA"
    },
    "47551002": {
        "Centro Poblado": "CARABALLO"
    },
    "47551003": {
        "Centro Poblado": "CHINOBLAS"
    },
    "47551005": {
        "Centro Poblado": "SAN JOSÉ DE LA MONTAÑA (GARRAPATA)"
    },
    "47551006": {
        "Centro Poblado": "LAS CANOAS"
    },
    "47551007": {
        "Centro Poblado": "LAS PIEDRAS"
    },
    "47551008": {
        "Centro Poblado": "MEDIALUNA"
    },
    "47551010": {
        "Centro Poblado": "CARMEN DEL MAGDALENA (PARACO)"
    },
    "47551011": {
        "Centro Poblado": "PARAÍSO"
    },
    "47551012": {
        "Centro Poblado": "PIÑUELAS"
    },
    "47551013": {
        "Centro Poblado": "PLACITAS"
    },
    "47551017": {
        "Centro Poblado": "LA RETIRADA"
    },
    "47555000": {
        "Centro Poblado": "PLATO"
    },
    "47555001": {
        "Centro Poblado": "APURE"
    },
    "47555002": {
        "Centro Poblado": "CARMEN DEL MAGDALENA"
    },
    "47555005": {
        "Centro Poblado": "ZARATE"
    },
    "47555006": {
        "Centro Poblado": "AGUAS VIVAS"
    },
    "47555007": {
        "Centro Poblado": "CIÉNEGUETA"
    },
    "47555008": {
        "Centro Poblado": "CERRO GRANDE"
    },
    "47555011": {
        "Centro Poblado": "SAN JOSÉ DEL PURGATORIO"
    },
    "47555015": {
        "Centro Poblado": "DISCIPLINA"
    },
    "47555017": {
        "Centro Poblado": "SAN ANTONIO DEL RÍO"
    },
    "47555018": {
        "Centro Poblado": "BUENA VISTA"
    },
    "47555020": {
        "Centro Poblado": "LOS POZOS"
    },
    "47555021": {
        "Centro Poblado": "CINCO Y SEIS"
    },
    "47570000": {
        "Centro Poblado": "PUEBLOVIEJO"
    },
    "47570002": {
        "Centro Poblado": "ISLA DEL ROSARIO"
    },
    "47570003": {
        "Centro Poblado": "PALMIRA"
    },
    "47570004": {
        "Centro Poblado": "TASAJERA"
    },
    "47570005": {
        "Centro Poblado": "TIERRA NUEVA"
    },
    "47570007": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "47570009": {
        "Centro Poblado": "NUEVA FRONTERA"
    },
    "47570010": {
        "Centro Poblado": "SAN JUAN DE PALOS PRIETOS (LA MONTAÑA)"
    },
    "47605000": {
        "Centro Poblado": "REMOLINO"
    },
    "47605002": {
        "Centro Poblado": "CORRAL VIEJO"
    },
    "47605003": {
        "Centro Poblado": "EL DIVIDIVI"
    },
    "47605004": {
        "Centro Poblado": "SAN RAFAEL DE BUENAVISTA"
    },
    "47605005": {
        "Centro Poblado": "SANTA RITA"
    },
    "47605006": {
        "Centro Poblado": "EL SALAO"
    },
    "47605007": {
        "Centro Poblado": "MARTINETE"
    },
    "47605008": {
        "Centro Poblado": "LAS CASITAS"
    },
    "47660000": {
        "Centro Poblado": "SAN ÁNGEL"
    },
    "47660002": {
        "Centro Poblado": "CASA DE TABLA"
    },
    "47660003": {
        "Centro Poblado": "CESPEDES"
    },
    "47660005": {
        "Centro Poblado": "FLORES DE MARÍA"
    },
    "47660007": {
        "Centro Poblado": "LA HORQUETA"
    },
    "47660009": {
        "Centro Poblado": "SAN ROQUE"
    },
    "47660010": {
        "Centro Poblado": "EL MANANTIAL"
    },
    "47660011": {
        "Centro Poblado": "PUEBLITO DE LOS BARRIOS"
    },
    "47660013": {
        "Centro Poblado": "ESTACIÓN VILLA"
    },
    "47660014": {
        "Centro Poblado": "MONTERRUBIO"
    },
    "47675000": {
        "Centro Poblado": "SALAMINA"
    },
    "47675001": {
        "Centro Poblado": "GUÁIMARO"
    },
    "47675005": {
        "Centro Poblado": "EL SALAO"
    },
    "47675006": {
        "Centro Poblado": "LA LOMA"
    },
    "47675007": {
        "Centro Poblado": "LA LOMITA"
    },
    "47692000": {
        "Centro Poblado": "SAN SEBASTIÁN DE BUENAVISTA"
    },
    "47692001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "47692002": {
        "Centro Poblado": "EL COCO"
    },
    "47692003": {
        "Centro Poblado": "LA PACHA"
    },
    "47692004": {
        "Centro Poblado": "LAS MARGARITAS"
    },
    "47692005": {
        "Centro Poblado": "LOS GALVIS"
    },
    "47692006": {
        "Centro Poblado": "MARÍA ANTONIA"
    },
    "47692007": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "47692008": {
        "Centro Poblado": "SANTA ROSA"
    },
    "47692009": {
        "Centro Poblado": "TRONCOSITO"
    },
    "47692010": {
        "Centro Poblado": "TRONCOSO"
    },
    "47692011": {
        "Centro Poblado": "VENERO"
    },
    "47692013": {
        "Centro Poblado": "EL SEIS"
    },
    "47692018": {
        "Centro Poblado": "SAN VALENTÍN"
    },
    "47692019": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "47703000": {
        "Centro Poblado": "SAN ZENÓN"
    },
    "47703001": {
        "Centro Poblado": "ANGOSTURA"
    },
    "47703002": {
        "Centro Poblado": "BERMEJAL"
    },
    "47703003": {
        "Centro Poblado": "EL PALOMAR"
    },
    "47703004": {
        "Centro Poblado": "JANEIRO"
    },
    "47703005": {
        "Centro Poblado": "LA MONTAÑA"
    },
    "47703006": {
        "Centro Poblado": "PEÑONCITO"
    },
    "47703007": {
        "Centro Poblado": "SANTA TERESA"
    },
    "47703008": {
        "Centro Poblado": "GUINEA"
    },
    "47703009": {
        "Centro Poblado": "EL HORNO"
    },
    "47703010": {
        "Centro Poblado": "PUERTO ARTURO"
    },
    "47707000": {
        "Centro Poblado": "SANTA ANA"
    },
    "47707001": {
        "Centro Poblado": "BARRO BLANCO"
    },
    "47707006": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "47707009": {
        "Centro Poblado": "JARABA"
    },
    "47707011": {
        "Centro Poblado": "SANTA ROSA"
    },
    "47720000": {
        "Centro Poblado": "SANTA BÁRBARA DE PINTO"
    },
    "47720001": {
        "Centro Poblado": "CUNDINAMARCA"
    },
    "47720002": {
        "Centro Poblado": "SAN PEDRO"
    },
    "47720003": {
        "Centro Poblado": "VELADERO"
    },
    "47720004": {
        "Centro Poblado": "CARRETAL"
    },
    "47720005": {
        "Centro Poblado": "CIENAGUETA"
    },
    "47745000": {
        "Centro Poblado": "SITIONUEVO"
    },
    "47745001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "47745002": {
        "Centro Poblado": "NUEVA VENECIA"
    },
    "47745003": {
        "Centro Poblado": "PALERMO"
    },
    "47745006": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "47798000": {
        "Centro Poblado": "TENERIFE"
    },
    "47798004": {
        "Centro Poblado": "REAL DEL OBISPO"
    },
    "47798005": {
        "Centro Poblado": "SAN LUIS"
    },
    "47798007": {
        "Centro Poblado": "EL JUNCAL"
    },
    "47798008": {
        "Centro Poblado": "SANTA INÉS"
    },
    "47960000": {
        "Centro Poblado": "PUNTA DE PIEDRAS"
    },
    "47960001": {
        "Centro Poblado": "CAÑO DE AGUAS"
    },
    "47960002": {
        "Centro Poblado": "CAPUCHO"
    },
    "47960003": {
        "Centro Poblado": "PIEDRAS DE MOLER"
    },
    "47960004": {
        "Centro Poblado": "PIEDRAS PINTADAS"
    },
    "47960005": {
        "Centro Poblado": "LOS CERRITOS"
    },
    "47960006": {
        "Centro Poblado": "EL BONGO"
    },
    "47980000": {
        "Centro Poblado": "PRADO - SEVILLA"
    },
    "47980001": {
        "Centro Poblado": "GUACAMAYAL"
    },
    "47980002": {
        "Centro Poblado": "GUAMACHITO"
    },
    "47980003": {
        "Centro Poblado": "LA GRAN VÍA"
    },
    "47980004": {
        "Centro Poblado": "ORIHUECA"
    },
    "47980005": {
        "Centro Poblado": "PALOMAR"
    },
    "47980006": {
        "Centro Poblado": "RÍO FRÍO"
    },
    "47980007": {
        "Centro Poblado": "SANTA ROSALÍA"
    },
    "47980009": {
        "Centro Poblado": "SOPLADOR"
    },
    "47980010": {
        "Centro Poblado": "TUCURINCA"
    },
    "47980011": {
        "Centro Poblado": "VARELA"
    },
    "47980012": {
        "Centro Poblado": "ZAWADY"
    },
    "47980013": {
        "Centro Poblado": "ESTACIÓN SEVILLA"
    },
    "47980014": {
        "Centro Poblado": "LA CANDELARIA"
    },
    "47980015": {
        "Centro Poblado": "SAN JOSÉ DE KENNEDY"
    },
    "47980016": {
        "Centro Poblado": "CAÑO MOCHO"
    },
    "47980017": {
        "Centro Poblado": "EL MAMÓN"
    },
    "47980018": {
        "Centro Poblado": "AGUSTINA"
    },
    "47980019": {
        "Centro Poblado": "CARITAL"
    },
    "47980020": {
        "Centro Poblado": "CASABLANCA"
    },
    "47980021": {
        "Centro Poblado": "CIUDAD PERDIDA"
    },
    "47980022": {
        "Centro Poblado": "EL REPOSO"
    },
    "47980023": {
        "Centro Poblado": "IBERIA"
    },
    "47980024": {
        "Centro Poblado": "MONTERIA"
    },
    "47980025": {
        "Centro Poblado": "PATUCA"
    },
    "47980026": {
        "Centro Poblado": "PAULINA"
    },
    "47980027": {
        "Centro Poblado": "PILOTO"
    },
    "47980028": {
        "Centro Poblado": "SALÓN CONCEPCIÓN"
    },
    "50001000": {
        "Centro Poblado": "VILLAVICENCIO"
    },
    "50001001": {
        "Centro Poblado": "CONCEPCIÓN"
    },
    "50001002": {
        "Centro Poblado": "RINCON DE POMPEYA"
    },
    "50001003": {
        "Centro Poblado": "SANTA ROSA DE RÍO NEGRO"
    },
    "50001004": {
        "Centro Poblado": "BUENAVISTA"
    },
    "50001005": {
        "Centro Poblado": "COCUY"
    },
    "50001007": {
        "Centro Poblado": "SERVITÁ"
    },
    "50001013": {
        "Centro Poblado": "PIPIRAL"
    },
    "50001014": {
        "Centro Poblado": "SAN LUIS DE OCOA"
    },
    "50001015": {
        "Centro Poblado": "ALTO POMPEYA"
    },
    "50001016": {
        "Centro Poblado": "CECILIA"
    },
    "50001017": {
        "Centro Poblado": "LA NOHORA"
    },
    "50001019": {
        "Centro Poblado": "APIAY"
    },
    "50001020": {
        "Centro Poblado": "BARCELONA"
    },
    "50001021": {
        "Centro Poblado": "ARGENTINA"
    },
    "50001023": {
        "Centro Poblado": "BELLA SUIZA"
    },
    "50001024": {
        "Centro Poblado": "CONDOMINIO DE LOS ODONTÓLOGOS"
    },
    "50001026": {
        "Centro Poblado": "LLANERITA"
    },
    "50001027": {
        "Centro Poblado": "NATURALIA"
    },
    "50006000": {
        "Centro Poblado": "ACACÍAS"
    },
    "50006001": {
        "Centro Poblado": "DINAMARCA"
    },
    "50006003": {
        "Centro Poblado": "SAN ISIDRO DE CHICHIMENE"
    },
    "50006006": {
        "Centro Poblado": "CONDOMINIO LA BONANZA"
    },
    "50006007": {
        "Centro Poblado": "LA CECILITA"
    },
    "50006008": {
        "Centro Poblado": "QUEBRADITAS"
    },
    "50006009": {
        "Centro Poblado": "SANTA ROSA"
    },
    "50006010": {
        "Centro Poblado": "EL DIAMANTE"
    },
    "50006011": {
        "Centro Poblado": "EL CENTRO"
    },
    "50006012": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "50006013": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "50006014": {
        "Centro Poblado": "LA FORTUNA"
    },
    "50006015": {
        "Centro Poblado": "LA SARDINATA"
    },
    "50006016": {
        "Centro Poblado": "LAS BLANCAS"
    },
    "50006017": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "50110000": {
        "Centro Poblado": "BARRANCA DE UPÍA"
    },
    "50110001": {
        "Centro Poblado": "SAN IGNACIO"
    },
    "50124000": {
        "Centro Poblado": "CABUYARO"
    },
    "50124002": {
        "Centro Poblado": "GUAYABAL DE UPÍA"
    },
    "50124003": {
        "Centro Poblado": "VISO DE UPÍA"
    },
    "50124004": {
        "Centro Poblado": "LOS MANGOS"
    },
    "50150000": {
        "Centro Poblado": "CASTILLA LA NUEVA"
    },
    "50150001": {
        "Centro Poblado": "SAN LORENZO"
    },
    "50150002": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "50150003": {
        "Centro Poblado": "EL TORO"
    },
    "50150004": {
        "Centro Poblado": "LAS VIOLETAS"
    },
    "50150005": {
        "Centro Poblado": "CASA BLANCA"
    },
    "50223000": {
        "Centro Poblado": "CUBARRAL"
    },
    "50223003": {
        "Centro Poblado": "PUERTO ARIARI"
    },
    "50226000": {
        "Centro Poblado": "CUMARAL"
    },
    "50226002": {
        "Centro Poblado": "GUACAVÍA"
    },
    "50226004": {
        "Centro Poblado": "SAN NICOLÁS"
    },
    "50226005": {
        "Centro Poblado": "VERACRUZ"
    },
    "50226010": {
        "Centro Poblado": "PRESENTADO"
    },
    "50245000": {
        "Centro Poblado": "EL CALVARIO"
    },
    "50245001": {
        "Centro Poblado": "MONTFORT"
    },
    "50245002": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "50251000": {
        "Centro Poblado": "EL CASTILLO"
    },
    "50251001": {
        "Centro Poblado": "MEDELLÍN DEL ARIARI"
    },
    "50251003": {
        "Centro Poblado": "MIRAVALLES"
    },
    "50251004": {
        "Centro Poblado": "PUERTO ESPERANZA"
    },
    "50270000": {
        "Centro Poblado": "EL DORADO"
    },
    "50270001": {
        "Centro Poblado": "PUEBLO SÁNCHEZ"
    },
    "50270002": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "50287000": {
        "Centro Poblado": "FUENTE DE ORO"
    },
    "50287001": {
        "Centro Poblado": "PUERTO ALJURE"
    },
    "50287002": {
        "Centro Poblado": "PUERTO LIMÓN"
    },
    "50287003": {
        "Centro Poblado": "PUERTO SANTANDER"
    },
    "50287004": {
        "Centro Poblado": "UNIÓN DEL ARIARI"
    },
    "50287005": {
        "Centro Poblado": "LA COOPERATIVA"
    },
    "50287006": {
        "Centro Poblado": "CAÑO BLANCO"
    },
    "50287007": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "50287008": {
        "Centro Poblado": "BARRANCO COLORADO CAÑO VENADO"
    },
    "50313000": {
        "Centro Poblado": "GRANADA"
    },
    "50313001": {
        "Centro Poblado": "CANAGUARO"
    },
    "50313002": {
        "Centro Poblado": "DOS QUEBRADAS"
    },
    "50313004": {
        "Centro Poblado": "LA PLAYA"
    },
    "50313005": {
        "Centro Poblado": "PUERTO CALDAS"
    },
    "50313006": {
        "Centro Poblado": "AGUAS CLARAS"
    },
    "50313007": {
        "Centro Poblado": "PUNTA BRAVA"
    },
    "50318000": {
        "Centro Poblado": "GUAMAL"
    },
    "50318001": {
        "Centro Poblado": "HUMADEA"
    },
    "50325000": {
        "Centro Poblado": "MAPIRIPÁN"
    },
    "50325001": {
        "Centro Poblado": "PUERTO ALVIRA"
    },
    "50325002": {
        "Centro Poblado": "MIELÓN"
    },
    "50325004": {
        "Centro Poblado": "ANZUELO"
    },
    "50325005": {
        "Centro Poblado": "GUACAMAYAS"
    },
    "50325006": {
        "Centro Poblado": "LA COOPERATIVA"
    },
    "50325007": {
        "Centro Poblado": "PUERTO SIARE"
    },
    "50325009": {
        "Centro Poblado": "EL SILENCIO"
    },
    "50325010": {
        "Centro Poblado": "LA JUNGLA"
    },
    "50325011": {
        "Centro Poblado": "RINCON DEL INDIO"
    },
    "50330000": {
        "Centro Poblado": "MESETAS"
    },
    "50330002": {
        "Centro Poblado": "JARDÍN DE LAS PEÑAS"
    },
    "50330005": {
        "Centro Poblado": "ORIENTE"
    },
    "50330007": {
        "Centro Poblado": "LA ARGENTINA"
    },
    "50330009": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "50330010": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "50350000": {
        "Centro Poblado": "LA MACARENA"
    },
    "50350001": {
        "Centro Poblado": "SAN FRANCISCO DE LA SOMBRA"
    },
    "50350003": {
        "Centro Poblado": "SAN JUAN DEL LOSADA"
    },
    "50350007": {
        "Centro Poblado": "LA CRISTALINA"
    },
    "50350008": {
        "Centro Poblado": "EL RUBÍ"
    },
    "50350010": {
        "Centro Poblado": "EL VERGEL"
    },
    "50350012": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "50350013": {
        "Centro Poblado": "LAURELES"
    },
    "50350014": {
        "Centro Poblado": "PLAYA RICA"
    },
    "50350015": {
        "Centro Poblado": "PUERTO LOZADA"
    },
    "50370000": {
        "Centro Poblado": "URIBE"
    },
    "50370001": {
        "Centro Poblado": "LA JULIA"
    },
    "50370002": {
        "Centro Poblado": "EL DIVISO"
    },
    "50400000": {
        "Centro Poblado": "LEJANÍAS"
    },
    "50400001": {
        "Centro Poblado": "CACAYAL"
    },
    "50400002": {
        "Centro Poblado": "ANGOSTURAS DEL GUAPE"
    },
    "50450000": {
        "Centro Poblado": "PUERTO CONCORDIA"
    },
    "50450001": {
        "Centro Poblado": "EL PORORIO"
    },
    "50450002": {
        "Centro Poblado": "LINDENAI"
    },
    "50450003": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "50568000": {
        "Centro Poblado": "PUERTO GAITÁN"
    },
    "50568001": {
        "Centro Poblado": "DOMO PLANAS"
    },
    "50568002": {
        "Centro Poblado": "SAN PEDRO DE ARIMENA"
    },
    "50568004": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "50568005": {
        "Centro Poblado": "EL PORVENIR"
    },
    "50568006": {
        "Centro Poblado": "PUERTO TRUJILLO"
    },
    "50568007": {
        "Centro Poblado": "PUENTE ARIMENA"
    },
    "50568008": {
        "Centro Poblado": "ALTO TILLAVÁ"
    },
    "50568010": {
        "Centro Poblado": "LA CRISTALINA"
    },
    "50568012": {
        "Centro Poblado": "MURUJUY"
    },
    "50573000": {
        "Centro Poblado": "PUERTO LÓPEZ"
    },
    "50573001": {
        "Centro Poblado": "LA BALSA"
    },
    "50573003": {
        "Centro Poblado": "PACHAQUIARO"
    },
    "50573004": {
        "Centro Poblado": "ALTAMIRA"
    },
    "50573006": {
        "Centro Poblado": "PUERTO GUADALUPE"
    },
    "50573007": {
        "Centro Poblado": "PUERTO PORFÍA"
    },
    "50573008": {
        "Centro Poblado": "REMOLINO"
    },
    "50573010": {
        "Centro Poblado": "BOCAS DEL GUAYURIBA"
    },
    "50573011": {
        "Centro Poblado": "GUICHIRAL"
    },
    "50573012": {
        "Centro Poblado": "CHAVIVA"
    },
    "50573013": {
        "Centro Poblado": "EL TIGRE"
    },
    "50573015": {
        "Centro Poblado": "PUEBLO NUEVO - GETSEMANÍ"
    },
    "50577000": {
        "Centro Poblado": "PUERTO LLERAS"
    },
    "50577003": {
        "Centro Poblado": "CASIBARE"
    },
    "50577004": {
        "Centro Poblado": "CAÑO RAYADO"
    },
    "50577005": {
        "Centro Poblado": "VILLA LA PAZ"
    },
    "50577006": {
        "Centro Poblado": "TIERRA GRATA"
    },
    "50577007": {
        "Centro Poblado": "LA UNIÓN"
    },
    "50577008": {
        "Centro Poblado": "VILLA PALMERAS"
    },
    "50590000": {
        "Centro Poblado": "PUERTO RICO"
    },
    "50590003": {
        "Centro Poblado": "LA LINDOSA"
    },
    "50590004": {
        "Centro Poblado": "BARRANCO COLORADO"
    },
    "50590005": {
        "Centro Poblado": "PUERTO TOLEDO"
    },
    "50590006": {
        "Centro Poblado": "CHARCO DANTO"
    },
    "50590007": {
        "Centro Poblado": "LA TIGRA"
    },
    "50590008": {
        "Centro Poblado": "PUERTO CHISPAS"
    },
    "50606000": {
        "Centro Poblado": "RESTREPO"
    },
    "50680000": {
        "Centro Poblado": "SAN CARLOS DE GUAROA"
    },
    "50680001": {
        "Centro Poblado": "PAJURE"
    },
    "50680002": {
        "Centro Poblado": "SURIMENA"
    },
    "50680003": {
        "Centro Poblado": "LA PALMERA"
    },
    "50683000": {
        "Centro Poblado": "SAN JUAN DE ARAMA"
    },
    "50683001": {
        "Centro Poblado": "EL VERGEL"
    },
    "50683005": {
        "Centro Poblado": "MESA FERNÁNDEZ"
    },
    "50683010": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "50683011": {
        "Centro Poblado": "CERRITO"
    },
    "50683012": {
        "Centro Poblado": "MIRAFLOREZ"
    },
    "50683013": {
        "Centro Poblado": "PEÑAS BLANCAS"
    },
    "50683015": {
        "Centro Poblado": "BELLA VISTA"
    },
    "50686000": {
        "Centro Poblado": "SAN JUANITO"
    },
    "50686003": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "50689000": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "50689001": {
        "Centro Poblado": "EL MEREY"
    },
    "50689006": {
        "Centro Poblado": "EL PARAISO MEJOR VIVIR"
    },
    "50711000": {
        "Centro Poblado": "VISTAHERMOSA"
    },
    "50711002": {
        "Centro Poblado": "PIÑALITO"
    },
    "50711003": {
        "Centro Poblado": "MARACAIBO"
    },
    "50711004": {
        "Centro Poblado": "CAÑO AMARILLO"
    },
    "50711005": {
        "Centro Poblado": "PUERTO LUCAS MARGEN IZQUIERDO"
    },
    "50711006": {
        "Centro Poblado": "PUERTO LUCAS MARGEN DERECHO"
    },
    "50711008": {
        "Centro Poblado": "PUERTO ESPERANZA MARGEN IZQUIERDO"
    },
    "50711012": {
        "Centro Poblado": "COSTA RICA"
    },
    "50711014": {
        "Centro Poblado": "PALESTINA"
    },
    "50711016": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "50711017": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "50711018": {
        "Centro Poblado": "ALBANIA"
    },
    "50711021": {
        "Centro Poblado": "LA REFORMA"
    },
    "50711022": {
        "Centro Poblado": "PALMERAS"
    },
    "52001000": {
        "Centro Poblado": "SAN JUAN DE PASTO"
    },
    "52001001": {
        "Centro Poblado": "CATAMBUCO"
    },
    "52001003": {
        "Centro Poblado": "EL ENCANO"
    },
    "52001004": {
        "Centro Poblado": "GENOY"
    },
    "52001005": {
        "Centro Poblado": "LA LAGUNA"
    },
    "52001007": {
        "Centro Poblado": "OBONUCO"
    },
    "52001008": {
        "Centro Poblado": "SANTA BARBARA"
    },
    "52001009": {
        "Centro Poblado": "JONGOVITO"
    },
    "52001010": {
        "Centro Poblado": "GUALMATÁN"
    },
    "52001012": {
        "Centro Poblado": "MAPACHICO - ATICANCE"
    },
    "52001013": {
        "Centro Poblado": "EL SOCORRO CIMARRÓN"
    },
    "52001016": {
        "Centro Poblado": "MOTILÓN"
    },
    "52001019": {
        "Centro Poblado": "CEROTAL"
    },
    "52001021": {
        "Centro Poblado": "LA VICTORIA"
    },
    "52001024": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "52001025": {
        "Centro Poblado": "EL PUERTO"
    },
    "52001027": {
        "Centro Poblado": "CABRERA"
    },
    "52001029": {
        "Centro Poblado": "DOLORES"
    },
    "52001030": {
        "Centro Poblado": "BUESAQUILLO"
    },
    "52001033": {
        "Centro Poblado": "CUJACAL"
    },
    "52001036": {
        "Centro Poblado": "TESCUAL"
    },
    "52001039": {
        "Centro Poblado": "ANGANOY"
    },
    "52001042": {
        "Centro Poblado": "DAZA"
    },
    "52001051": {
        "Centro Poblado": "CUBIJAN BAJO"
    },
    "52001052": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "52001053": {
        "Centro Poblado": "MOCONDINO"
    },
    "52001055": {
        "Centro Poblado": "CANCHALA"
    },
    "52001056": {
        "Centro Poblado": "LOS ANGELES"
    },
    "52001058": {
        "Centro Poblado": "EL ROSARIO"
    },
    "52001059": {
        "Centro Poblado": "JAMONDINO"
    },
    "52001063": {
        "Centro Poblado": "BOTANILLA"
    },
    "52001064": {
        "Centro Poblado": "CHARGUAYACO"
    },
    "52001065": {
        "Centro Poblado": "CRUZ DE AMARILLO"
    },
    "52001066": {
        "Centro Poblado": "EL CAMPANERO"
    },
    "52001068": {
        "Centro Poblado": "JURADO"
    },
    "52001071": {
        "Centro Poblado": "LA MERCED"
    },
    "52001072": {
        "Centro Poblado": "LAS ENCINAS"
    },
    "52001073": {
        "Centro Poblado": "MAPACHICO ALTO"
    },
    "52001074": {
        "Centro Poblado": "MAPACHICO SAN JOSÉ"
    },
    "52001076": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "52001078": {
        "Centro Poblado": "SAN JUAN DE ANGANOY"
    },
    "52001079": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "52001080": {
        "Centro Poblado": "VILLA MARÍA"
    },
    "52001086": {
        "Centro Poblado": "GUALMATAN ALTO"
    },
    "52001087": {
        "Centro Poblado": "LA CALDERA"
    },
    "52001089": {
        "Centro Poblado": "PUERRES"
    },
    "52019000": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "52019004": {
        "Centro Poblado": "CAMPOBELLO"
    },
    "52019009": {
        "Centro Poblado": "CARMELO ASENTAMIENTO 1"
    },
    "52019013": {
        "Centro Poblado": "FÁTIMA"
    },
    "52022000": {
        "Centro Poblado": "ALDANA"
    },
    "52022001": {
        "Centro Poblado": "PAMBA ROSA"
    },
    "52022003": {
        "Centro Poblado": "SAN LUIS"
    },
    "52036000": {
        "Centro Poblado": "ANCUYA"
    },
    "52036017": {
        "Centro Poblado": "INDO SANTA ROSA"
    },
    "52051000": {
        "Centro Poblado": "BERRUECOS"
    },
    "52051005": {
        "Centro Poblado": "EL EMPATE"
    },
    "52051007": {
        "Centro Poblado": "ROSA FLORIDA SUR - SECTOR LA CAPILLA"
    },
    "52051012": {
        "Centro Poblado": "ROSAFLORIDA NORTE"
    },
    "52051015": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "52079000": {
        "Centro Poblado": "BARBACOAS"
    },
    "52079001": {
        "Centro Poblado": "ALTAQUER"
    },
    "52079003": {
        "Centro Poblado": "CHALCHAL"
    },
    "52079005": {
        "Centro Poblado": "DIAGUILLO"
    },
    "52079006": {
        "Centro Poblado": "JUNÍN"
    },
    "52079009": {
        "Centro Poblado": "LOS BRAZOS"
    },
    "52079011": {
        "Centro Poblado": "MONGÓN"
    },
    "52079013": {
        "Centro Poblado": "PAMBANA"
    },
    "52079014": {
        "Centro Poblado": "SUCRE GUINULTE"
    },
    "52079018": {
        "Centro Poblado": "SAN MIGUEL NAMBÍ"
    },
    "52079020": {
        "Centro Poblado": "TERAIMBE"
    },
    "52079022": {
        "Centro Poblado": "SAN JUAN PALACIO"
    },
    "52079023": {
        "Centro Poblado": "ÑAMBÍ"
    },
    "52079024": {
        "Centro Poblado": "CARGAZON"
    },
    "52079025": {
        "Centro Poblado": "CASCAJERO"
    },
    "52079026": {
        "Centro Poblado": "EL DIVISO"
    },
    "52079027": {
        "Centro Poblado": "LA PLAYA"
    },
    "52079028": {
        "Centro Poblado": "PAUNDE"
    },
    "52079029": {
        "Centro Poblado": "SALÍ"
    },
    "52079030": {
        "Centro Poblado": "YALARE"
    },
    "52079035": {
        "Centro Poblado": "PALO SECO"
    },
    "52083000": {
        "Centro Poblado": "BELÉN"
    },
    "52083001": {
        "Centro Poblado": "SANTA ROSA"
    },
    "52110000": {
        "Centro Poblado": "BUESACO"
    },
    "52110001": {
        "Centro Poblado": "PALASINOY"
    },
    "52110002": {
        "Centro Poblado": "ROSAL DEL MONTE"
    },
    "52110003": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "52110004": {
        "Centro Poblado": "SAN IGNACIO"
    },
    "52110005": {
        "Centro Poblado": "SANTAFÉ"
    },
    "52110006": {
        "Centro Poblado": "SANTAMARÍA"
    },
    "52110007": {
        "Centro Poblado": "VILLAMORENO"
    },
    "52110008": {
        "Centro Poblado": "VERACRUZ"
    },
    "52110009": {
        "Centro Poblado": "ALTACLARA"
    },
    "52110022": {
        "Centro Poblado": "JUANAMBÚ"
    },
    "52110030": {
        "Centro Poblado": "SAN MIGUEL SANTAFÉ"
    },
    "52203000": {
        "Centro Poblado": "GÉNOVA"
    },
    "52203001": {
        "Centro Poblado": "GUAITARILLA"
    },
    "52203002": {
        "Centro Poblado": "LA PLATA"
    },
    "52203004": {
        "Centro Poblado": "VILLANUEVA"
    },
    "52207000": {
        "Centro Poblado": "CONSACÁ"
    },
    "52207004": {
        "Centro Poblado": "BOMBONA"
    },
    "52207013": {
        "Centro Poblado": "EL HATILLO"
    },
    "52207023": {
        "Centro Poblado": "RUMIPAMBA"
    },
    "52210000": {
        "Centro Poblado": "CONTADERO"
    },
    "52210001": {
        "Centro Poblado": "ALDEA DE MARÍA"
    },
    "52210002": {
        "Centro Poblado": "LA JOSEFINA"
    },
    "52215000": {
        "Centro Poblado": "CÓRDOBA"
    },
    "52215001": {
        "Centro Poblado": "LOS ARRAYANES"
    },
    "52215004": {
        "Centro Poblado": "SANTANDER"
    },
    "52215005": {
        "Centro Poblado": "PUEBLO BAJO"
    },
    "52224000": {
        "Centro Poblado": "CARLOSAMA"
    },
    "52224001": {
        "Centro Poblado": "MACAS"
    },
    "52227000": {
        "Centro Poblado": "CUMBAL"
    },
    "52227001": {
        "Centro Poblado": "CHILES"
    },
    "52227004": {
        "Centro Poblado": "PANÁN"
    },
    "52227006": {
        "Centro Poblado": "NAZATE"
    },
    "52227009": {
        "Centro Poblado": "EL CHOTA"
    },
    "52227010": {
        "Centro Poblado": "LA POMA"
    },
    "52233000": {
        "Centro Poblado": "CUMBITARA"
    },
    "52233001": {
        "Centro Poblado": "DAMASCO"
    },
    "52233002": {
        "Centro Poblado": "EL DESIERTO"
    },
    "52233003": {
        "Centro Poblado": "PISANDA"
    },
    "52233004": {
        "Centro Poblado": "SIDÓN"
    },
    "52233007": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "52233008": {
        "Centro Poblado": "SANTA ROSA"
    },
    "52233011": {
        "Centro Poblado": "SANTA ANA"
    },
    "52233012": {
        "Centro Poblado": "CAMPO BELLO"
    },
    "52240000": {
        "Centro Poblado": "CHACHAGÜÍ"
    },
    "52240001": {
        "Centro Poblado": "ARIZONA"
    },
    "52240002": {
        "Centro Poblado": "AGRARIO"
    },
    "52240003": {
        "Centro Poblado": "CAÑO ALTO"
    },
    "52240004": {
        "Centro Poblado": "CAÑO BAJO"
    },
    "52240005": {
        "Centro Poblado": "CHORRILLO"
    },
    "52240006": {
        "Centro Poblado": "GUAIRABAMBA"
    },
    "52240008": {
        "Centro Poblado": "LA LOMA"
    },
    "52240011": {
        "Centro Poblado": "SANTA MÓNICA"
    },
    "52240012": {
        "Centro Poblado": "COCHA CANO"
    },
    "52240013": {
        "Centro Poblado": "PEDREGAL"
    },
    "52250000": {
        "Centro Poblado": "EL CHARCO"
    },
    "52250003": {
        "Centro Poblado": "SAN PEDRO"
    },
    "52250022": {
        "Centro Poblado": "EL CUIL"
    },
    "52250023": {
        "Centro Poblado": "BAZÁN"
    },
    "52254000": {
        "Centro Poblado": "EL PEÑOL"
    },
    "52254001": {
        "Centro Poblado": "LAS COCHAS"
    },
    "52254002": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "52254003": {
        "Centro Poblado": "PEÑOL VIEJO"
    },
    "52254004": {
        "Centro Poblado": "SAN FRANCISCO BAJO"
    },
    "52256000": {
        "Centro Poblado": "EL ROSARIO"
    },
    "52256003": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "52256004": {
        "Centro Poblado": "LA SIERRA"
    },
    "52256008": {
        "Centro Poblado": "EL VADO"
    },
    "52256012": {
        "Centro Poblado": "MARTÍN PÉREZ"
    },
    "52256024": {
        "Centro Poblado": "EL RINCÓN"
    },
    "52256025": {
        "Centro Poblado": "EL SUSPIRO"
    },
    "52258000": {
        "Centro Poblado": "EL TABLÓN DE GÓMEZ"
    },
    "52258001": {
        "Centro Poblado": "APONTE"
    },
    "52258002": {
        "Centro Poblado": "LA CUEVA"
    },
    "52258003": {
        "Centro Poblado": "LAS MESAS"
    },
    "52258005": {
        "Centro Poblado": "LA VICTORIA"
    },
    "52258015": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "52260000": {
        "Centro Poblado": "EL TAMBO"
    },
    "52287000": {
        "Centro Poblado": "FUNES"
    },
    "52287001": {
        "Centro Poblado": "CHAPAL"
    },
    "52317000": {
        "Centro Poblado": "GUACHUCAL"
    },
    "52317001": {
        "Centro Poblado": "COLIMBA"
    },
    "52317002": {
        "Centro Poblado": "EL CONSUELO DE CHILLANQUER"
    },
    "52317003": {
        "Centro Poblado": "SAN DIEGO DE MUELLAMUES"
    },
    "52317004": {
        "Centro Poblado": "SAN JOSÉ DE CHILLANQUER"
    },
    "52317005": {
        "Centro Poblado": "LA VICTORIA"
    },
    "52317007": {
        "Centro Poblado": "ARVELA"
    },
    "52317008": {
        "Centro Poblado": "QUETAMBÚD"
    },
    "52320000": {
        "Centro Poblado": "GUAITARILLA"
    },
    "52320016": {
        "Centro Poblado": "EL ROSAL"
    },
    "52323000": {
        "Centro Poblado": "GUALMATÁN"
    },
    "52323001": {
        "Centro Poblado": "CUATIS"
    },
    "52352000": {
        "Centro Poblado": "ILES"
    },
    "52352003": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "52352006": {
        "Centro Poblado": "EL CAPULI"
    },
    "52352009": {
        "Centro Poblado": "EL PORVENIR"
    },
    "52352010": {
        "Centro Poblado": "EL PORVENIR 1"
    },
    "52354000": {
        "Centro Poblado": "IMUÉS"
    },
    "52354002": {
        "Centro Poblado": "PILCUAN LA RECTA"
    },
    "52354004": {
        "Centro Poblado": "PILCUAN VIEJO"
    },
    "52354007": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "52354012": {
        "Centro Poblado": "SANTA ANA"
    },
    "52356000": {
        "Centro Poblado": "IPIALES"
    },
    "52356001": {
        "Centro Poblado": "LA VICTORIA"
    },
    "52356002": {
        "Centro Poblado": "LAS LAJAS"
    },
    "52356003": {
        "Centro Poblado": "SAN JUAN"
    },
    "52356004": {
        "Centro Poblado": "YARAMAL"
    },
    "52356005": {
        "Centro Poblado": "LOMAS DE SURAS"
    },
    "52356008": {
        "Centro Poblado": "ZAGUARÁN"
    },
    "52356009": {
        "Centro Poblado": "LAS CRUCES"
    },
    "52356011": {
        "Centro Poblado": "EL PLACER"
    },
    "52356012": {
        "Centro Poblado": "LOS CHILCOS"
    },
    "52356013": {
        "Centro Poblado": "YANALA"
    },
    "52356014": {
        "Centro Poblado": "JARDINES DE SUCUMBIOS"
    },
    "52378000": {
        "Centro Poblado": "LA CRUZ"
    },
    "52378005": {
        "Centro Poblado": "SAN GERARDO"
    },
    "52378009": {
        "Centro Poblado": "TAJUMBINA"
    },
    "52378013": {
        "Centro Poblado": "CABUYALES"
    },
    "52378017": {
        "Centro Poblado": "LA ESTANCIA"
    },
    "52381000": {
        "Centro Poblado": "LA FLORIDA"
    },
    "52381001": {
        "Centro Poblado": "MATITUY"
    },
    "52381002": {
        "Centro Poblado": "ROBLES"
    },
    "52381003": {
        "Centro Poblado": "TUNJA LA GRANDE"
    },
    "52381008": {
        "Centro Poblado": "EL RODEO"
    },
    "52381011": {
        "Centro Poblado": "ACHUPAYAS"
    },
    "52381012": {
        "Centro Poblado": "PANCHINDO"
    },
    "52385000": {
        "Centro Poblado": "LA LLANADA"
    },
    "52385001": {
        "Centro Poblado": "VERGEL"
    },
    "52385015": {
        "Centro Poblado": "BOLIVAR"
    },
    "52390000": {
        "Centro Poblado": "LA TOLA"
    },
    "52390003": {
        "Centro Poblado": "VIGIA DE LA MAR"
    },
    "52390007": {
        "Centro Poblado": "PIOJA"
    },
    "52390008": {
        "Centro Poblado": "PANGAMOSA"
    },
    "52390009": {
        "Centro Poblado": "MULATOS"
    },
    "52390012": {
        "Centro Poblado": "NERETE"
    },
    "52390013": {
        "Centro Poblado": "AMARALES"
    },
    "52390014": {
        "Centro Poblado": "BAJO PALOMINO"
    },
    "52390015": {
        "Centro Poblado": "PUEBLITO"
    },
    "52390016": {
        "Centro Poblado": "SAN PABLO MAR"
    },
    "52399000": {
        "Centro Poblado": "LA UNIÓN"
    },
    "52399001": {
        "Centro Poblado": "SANTANDER"
    },
    "52399003": {
        "Centro Poblado": "LA CALDERA"
    },
    "52399012": {
        "Centro Poblado": "LA PLAYA"
    },
    "52399018": {
        "Centro Poblado": "OLIVOS"
    },
    "52399029": {
        "Centro Poblado": "LA BETULIA"
    },
    "52399030": {
        "Centro Poblado": "QUIROZ ALTO"
    },
    "52399035": {
        "Centro Poblado": "EL MANGO"
    },
    "52399036": {
        "Centro Poblado": "LA BETULIA BAJO"
    },
    "52405000": {
        "Centro Poblado": "LEIVA"
    },
    "52405001": {
        "Centro Poblado": "EL PALMAR"
    },
    "52405002": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "52405006": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "52405007": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "52405008": {
        "Centro Poblado": "LA FLORIDA"
    },
    "52405009": {
        "Centro Poblado": "EL TABLÓN"
    },
    "52405014": {
        "Centro Poblado": "VILLA BAJA"
    },
    "52411000": {
        "Centro Poblado": "LINARES"
    },
    "52411001": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "52411002": {
        "Centro Poblado": "TABILES"
    },
    "52411003": {
        "Centro Poblado": "TAMBILLO BRAVOS"
    },
    "52411004": {
        "Centro Poblado": "BELLA FLORIDA"
    },
    "52411005": {
        "Centro Poblado": "ARBOLEDAS"
    },
    "52411006": {
        "Centro Poblado": "BELLA VISTA"
    },
    "52418000": {
        "Centro Poblado": "SOTOMAYOR"
    },
    "52427000": {
        "Centro Poblado": "PAYÁN"
    },
    "52427003": {
        "Centro Poblado": "NANSALBID"
    },
    "52427005": {
        "Centro Poblado": "GUILPI PIRAGUA"
    },
    "52427006": {
        "Centro Poblado": "RICAURTE"
    },
    "52427015": {
        "Centro Poblado": "BRISAS DE HAMBURGO"
    },
    "52427016": {
        "Centro Poblado": "BELLA VISTA"
    },
    "52427017": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "52435000": {
        "Centro Poblado": "PIEDRANCHA"
    },
    "52435002": {
        "Centro Poblado": "CHUCUNES"
    },
    "52435008": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "52435009": {
        "Centro Poblado": "EL CARMELO"
    },
    "52435010": {
        "Centro Poblado": "EL ARCO"
    },
    "52435011": {
        "Centro Poblado": "EL ARENAL"
    },
    "52473000": {
        "Centro Poblado": "MOSQUERA"
    },
    "52473001": {
        "Centro Poblado": "COCALITO JIMÉNEZ (GABRIEL TURBAY)"
    },
    "52473004": {
        "Centro Poblado": "COCAL DE LOS PAYANES"
    },
    "52473006": {
        "Centro Poblado": "FIRME CIFUENTES"
    },
    "52473007": {
        "Centro Poblado": "BOCAS DE GUANDIPA"
    },
    "52473008": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "52473009": {
        "Centro Poblado": "EL GARCERO"
    },
    "52473010": {
        "Centro Poblado": "EL BAJITO DE ECHANDÍA"
    },
    "52473014": {
        "Centro Poblado": "PAMPA CHAPILA"
    },
    "52473015": {
        "Centro Poblado": "PLAYA NUEVA"
    },
    "52473018": {
        "Centro Poblado": "EL TORTUGO"
    },
    "52473026": {
        "Centro Poblado": "EL CANTIL"
    },
    "52473027": {
        "Centro Poblado": "EL NARANJO"
    },
    "52473033": {
        "Centro Poblado": "PAMPA QUIÑONES"
    },
    "52480000": {
        "Centro Poblado": "NARIÑO"
    },
    "52490000": {
        "Centro Poblado": "BOCAS DE SATINGA"
    },
    "52490003": {
        "Centro Poblado": "EL CARMEN"
    },
    "52490008": {
        "Centro Poblado": "SAN JOSÉ CALABAZAL"
    },
    "52490011": {
        "Centro Poblado": "ALTO ZAPANQUE"
    },
    "52490012": {
        "Centro Poblado": "BAJO ZAPANQUE"
    },
    "52490013": {
        "Centro Poblado": "LA TOLITA"
    },
    "52490014": {
        "Centro Poblado": "ZAPOTAL"
    },
    "52490015": {
        "Centro Poblado": "BOCA DE VIBORA"
    },
    "52490016": {
        "Centro Poblado": "EL NATO"
    },
    "52490017": {
        "Centro Poblado": "CAROLINA"
    },
    "52490018": {
        "Centro Poblado": "LAS PALMAS"
    },
    "52490019": {
        "Centro Poblado": "SAMARITANO"
    },
    "52490020": {
        "Centro Poblado": "SANTAMARIA"
    },
    "52506000": {
        "Centro Poblado": "OSPINA"
    },
    "52506002": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "52506005": {
        "Centro Poblado": "CUNCHILA O MORENO"
    },
    "52520000": {
        "Centro Poblado": "SALAHONDA"
    },
    "52520007": {
        "Centro Poblado": "BOCAS DE CURAY"
    },
    "52520011": {
        "Centro Poblado": "LUIS AVELINO PÉREZ"
    },
    "52520012": {
        "Centro Poblado": "LA PLAYA"
    },
    "52520015": {
        "Centro Poblado": "OLIVO CURAY"
    },
    "52520016": {
        "Centro Poblado": "SANDER CURAY"
    },
    "52520017": {
        "Centro Poblado": "SOLEDAD CURAY I"
    },
    "52520018": {
        "Centro Poblado": "SOLEDAD CURAY II"
    },
    "52540000": {
        "Centro Poblado": "POLICARPA"
    },
    "52540001": {
        "Centro Poblado": "ALTAMIRA"
    },
    "52540002": {
        "Centro Poblado": "MADRIGAL"
    },
    "52540003": {
        "Centro Poblado": "SAN ROQUE (BUENAVISTA)"
    },
    "52540004": {
        "Centro Poblado": "SÁNCHEZ"
    },
    "52540005": {
        "Centro Poblado": "EL EJIDO"
    },
    "52540006": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "52540007": {
        "Centro Poblado": "RESTREPO"
    },
    "52540008": {
        "Centro Poblado": "EL CERRO"
    },
    "52540009": {
        "Centro Poblado": "LA VEGA"
    },
    "52540010": {
        "Centro Poblado": "SAN PABLO"
    },
    "52560000": {
        "Centro Poblado": "POTOSÍ"
    },
    "52560001": {
        "Centro Poblado": "CÁRDENAS"
    },
    "52560002": {
        "Centro Poblado": "BAJO SINAÍ"
    },
    "52560006": {
        "Centro Poblado": "SAN PEDRO"
    },
    "52565000": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "52565001": {
        "Centro Poblado": "GUADRAHUMA"
    },
    "52573000": {
        "Centro Poblado": "PUERRES"
    },
    "52573002": {
        "Centro Poblado": "MONOPAMBA"
    },
    "52573003": {
        "Centro Poblado": "SAN MATEO"
    },
    "52573005": {
        "Centro Poblado": "MAICIRA"
    },
    "52573006": {
        "Centro Poblado": "EL LLANO"
    },
    "52573010": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "52573013": {
        "Centro Poblado": "YANALE"
    },
    "52573014": {
        "Centro Poblado": "LOS ALIZALES"
    },
    "52585000": {
        "Centro Poblado": "PUPIALES"
    },
    "52585004": {
        "Centro Poblado": "JOSÉ MARÍA HERNÁNDEZ"
    },
    "52612000": {
        "Centro Poblado": "RICAURTE"
    },
    "52612003": {
        "Centro Poblado": "OSPINA PÉREZ"
    },
    "52612004": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "52612008": {
        "Centro Poblado": "CHAMBU"
    },
    "52612011": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "52612012": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "52612013": {
        "Centro Poblado": "PALMAR"
    },
    "52621000": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "52621009": {
        "Centro Poblado": "LAS LAJAS PUMBI"
    },
    "52621016": {
        "Centro Poblado": "SAN ANTONIO - BOCA TELEMBI"
    },
    "52621028": {
        "Centro Poblado": "LAS MERCEDES - CHIMBUZA"
    },
    "52678000": {
        "Centro Poblado": "SAMANIEGO"
    },
    "52678007": {
        "Centro Poblado": "TANAMA"
    },
    "52678012": {
        "Centro Poblado": "CHUGULDÍ"
    },
    "52678013": {
        "Centro Poblado": "TURUPAMBA"
    },
    "52678015": {
        "Centro Poblado": "PUERCHAG"
    },
    "52678017": {
        "Centro Poblado": "CARTAGENA"
    },
    "52678024": {
        "Centro Poblado": "LA MESA"
    },
    "52678025": {
        "Centro Poblado": "OBANDO"
    },
    "52678029": {
        "Centro Poblado": "BONETE"
    },
    "52678030": {
        "Centro Poblado": "MIRADOR DE SARACONCHO"
    },
    "52683000": {
        "Centro Poblado": "SANDONÁ"
    },
    "52683001": {
        "Centro Poblado": "BOLÍVAR"
    },
    "52683002": {
        "Centro Poblado": "EL INGENIO"
    },
    "52683003": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "52683004": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "52683005": {
        "Centro Poblado": "SANTA ROSA"
    },
    "52683007": {
        "Centro Poblado": "ROMA CHÁVEZ"
    },
    "52683009": {
        "Centro Poblado": "PARAGUAY"
    },
    "52683010": {
        "Centro Poblado": "EL VERGEL"
    },
    "52683011": {
        "Centro Poblado": "SAN GABRIEL"
    },
    "52683012": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "52683014": {
        "Centro Poblado": "ALTAMIRA CRUZ DE ARADA"
    },
    "52683016": {
        "Centro Poblado": "CHÁVEZ"
    },
    "52683017": {
        "Centro Poblado": "TAMBILLO"
    },
    "52683018": {
        "Centro Poblado": "LA LOMA"
    },
    "52683022": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "52683023": {
        "Centro Poblado": "SAN FRANCISCO ALTO"
    },
    "52683027": {
        "Centro Poblado": "URBANIZACION VILLA CAFELINA"
    },
    "52685000": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "52685001": {
        "Centro Poblado": "LA VEGA"
    },
    "52685002": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "52687000": {
        "Centro Poblado": "SAN LORENZO"
    },
    "52687001": {
        "Centro Poblado": "EL CARMEN"
    },
    "52687002": {
        "Centro Poblado": "SANTA CECILIA"
    },
    "52687003": {
        "Centro Poblado": "SANTA MARTHA"
    },
    "52687005": {
        "Centro Poblado": "SAN VICENTE"
    },
    "52687008": {
        "Centro Poblado": "EL CHEPE"
    },
    "52693000": {
        "Centro Poblado": "SAN PABLO"
    },
    "52693002": {
        "Centro Poblado": "BRICEÑO"
    },
    "52693004": {
        "Centro Poblado": "LA CAÑADA"
    },
    "52693017": {
        "Centro Poblado": "CHILCAL ALTO"
    },
    "52694000": {
        "Centro Poblado": "SAN PEDRO DE CARTAGO"
    },
    "52694001": {
        "Centro Poblado": "LA COMUNIDAD"
    },
    "52696000": {
        "Centro Poblado": "ISCUANDÉ"
    },
    "52696009": {
        "Centro Poblado": "PALOMINO"
    },
    "52696012": {
        "Centro Poblado": "CUERBAL"
    },
    "52696013": {
        "Centro Poblado": "JUANCHILLO"
    },
    "52696014": {
        "Centro Poblado": "LA ENSENADA"
    },
    "52696015": {
        "Centro Poblado": "CHICO PÉREZ"
    },
    "52696017": {
        "Centro Poblado": "SANTA RITA"
    },
    "52696018": {
        "Centro Poblado": "BOCA DE CHANZARA"
    },
    "52696019": {
        "Centro Poblado": "LAS VARAS"
    },
    "52696020": {
        "Centro Poblado": "QUIGUPI"
    },
    "52696021": {
        "Centro Poblado": "RODEA"
    },
    "52696022": {
        "Centro Poblado": "SECADERO SEGUIHONDA"
    },
    "52696023": {
        "Centro Poblado": "SOLEDAD PUEBLITO"
    },
    "52699000": {
        "Centro Poblado": "GUACHAVÉS"
    },
    "52699001": {
        "Centro Poblado": "BALALAIKA"
    },
    "52699004": {
        "Centro Poblado": "MANCHAG"
    },
    "52720000": {
        "Centro Poblado": "SAPUYES"
    },
    "52720001": {
        "Centro Poblado": "EL ESPINO"
    },
    "52720002": {
        "Centro Poblado": "URIBE"
    },
    "52786000": {
        "Centro Poblado": "TAMINANGO"
    },
    "52786002": {
        "Centro Poblado": "EL TABLÓN"
    },
    "52786003": {
        "Centro Poblado": "CURIACO"
    },
    "52786006": {
        "Centro Poblado": "ALTO DE DIEGO"
    },
    "52786007": {
        "Centro Poblado": "EL MANZANO"
    },
    "52786014": {
        "Centro Poblado": "PÁRAMO"
    },
    "52786018": {
        "Centro Poblado": "LA GRANADA"
    },
    "52786019": {
        "Centro Poblado": "EL REMOLINO"
    },
    "52786021": {
        "Centro Poblado": "GUAYACANAL"
    },
    "52786022": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "52786023": {
        "Centro Poblado": "EL DIVISO"
    },
    "52786024": {
        "Centro Poblado": "VIENTO LIBRE"
    },
    "52786025": {
        "Centro Poblado": "PANOYA"
    },
    "52788000": {
        "Centro Poblado": "TANGUA"
    },
    "52788001": {
        "Centro Poblado": "SANTANDER"
    },
    "52835000": {
        "Centro Poblado": "SAN ANDRÉS DE TUMACO, DISTRITO ESPECIAL, INDUSTRIAL, PORTUARIO, BIODIVERSO Y ECOTURÍSTICO"
    },
    "52835009": {
        "Centro Poblado": "CAUNAPÍ"
    },
    "52835010": {
        "Centro Poblado": "COLORADO"
    },
    "52835011": {
        "Centro Poblado": "DESCOLGADERO"
    },
    "52835012": {
        "Centro Poblado": "CHAJAL"
    },
    "52835016": {
        "Centro Poblado": "PITAL"
    },
    "52835017": {
        "Centro Poblado": "ESPRIELLA"
    },
    "52835020": {
        "Centro Poblado": "BARRO COLORADO"
    },
    "52835021": {
        "Centro Poblado": "SAN JOSE DEL GUAYABO"
    },
    "52835030": {
        "Centro Poblado": "GUAYACANA"
    },
    "52835031": {
        "Centro Poblado": "LLORENTE"
    },
    "52835036": {
        "Centro Poblado": "PALAMBÍ"
    },
    "52835037": {
        "Centro Poblado": "IMBILI MIRASPALMAS"
    },
    "52835040": {
        "Centro Poblado": "EL PROGRESO SANTO DOMINGO"
    },
    "52835042": {
        "Centro Poblado": "SAN LUIS ROBLES"
    },
    "52835047": {
        "Centro Poblado": "SALISVÍ"
    },
    "52835050": {
        "Centro Poblado": "VILLA SAN JUAN"
    },
    "52835051": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "52835058": {
        "Centro Poblado": "TEHERAN"
    },
    "52835059": {
        "Centro Poblado": "URIBE URIBE (CHILVI)"
    },
    "52835063": {
        "Centro Poblado": "EL BAJITO"
    },
    "52835065": {
        "Centro Poblado": "EL PINDE"
    },
    "52835068": {
        "Centro Poblado": "CALETA VIENTO LIBRE"
    },
    "52835069": {
        "Centro Poblado": "CEIBITO"
    },
    "52835071": {
        "Centro Poblado": "EL CARMEN KM 36"
    },
    "52835075": {
        "Centro Poblado": "BOCANA NUEVA"
    },
    "52835077": {
        "Centro Poblado": "CHILVICITO"
    },
    "52835083": {
        "Centro Poblado": "LA SIRENA"
    },
    "52835085": {
        "Centro Poblado": "PALAY"
    },
    "52835087": {
        "Centro Poblado": "PULGANDE"
    },
    "52835088": {
        "Centro Poblado": "RETOÑO"
    },
    "52835091": {
        "Centro Poblado": "SANTA ROSA"
    },
    "52835092": {
        "Centro Poblado": "ALTO AGUA CLARA"
    },
    "52835093": {
        "Centro Poblado": "IMBILPI DEL CARMEN"
    },
    "52835099": {
        "Centro Poblado": "INGUAPI DEL CARMEN"
    },
    "52835100": {
        "Centro Poblado": "SANTA MARÍA ROSARIO"
    },
    "52835101": {
        "Centro Poblado": "LA BARCA"
    },
    "52835102": {
        "Centro Poblado": "EL COCO"
    },
    "52835104": {
        "Centro Poblado": "ALBANIA"
    },
    "52835107": {
        "Centro Poblado": "BAJO JAGUA"
    },
    "52835108": {
        "Centro Poblado": "BRISAS DEL ACUEDUCTO"
    },
    "52835109": {
        "Centro Poblado": "CACAGUAL"
    },
    "52835111": {
        "Centro Poblado": "CORRIENTE GRANDE"
    },
    "52835114": {
        "Centro Poblado": "GUABAL"
    },
    "52835115": {
        "Centro Poblado": "GUACHAL"
    },
    "52835116": {
        "Centro Poblado": "GUALTAL"
    },
    "52835118": {
        "Centro Poblado": "EL RETORNO"
    },
    "52835119": {
        "Centro Poblado": "JUAN DOMINGO"
    },
    "52835120": {
        "Centro Poblado": "KILÓMETRO 28"
    },
    "52835121": {
        "Centro Poblado": "KILÓMETRO 35"
    },
    "52835123": {
        "Centro Poblado": "KILÓMETRO 58"
    },
    "52835125": {
        "Centro Poblado": "LA CHORRERA"
    },
    "52835127": {
        "Centro Poblado": "PIÑUELA RIO MIRA"
    },
    "52835129": {
        "Centro Poblado": "LA VEGA"
    },
    "52835130": {
        "Centro Poblado": "MAJAGUA"
    },
    "52835133": {
        "Centro Poblado": "PÁCORA"
    },
    "52835134": {
        "Centro Poblado": "PINDALES"
    },
    "52835136": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "52835140": {
        "Centro Poblado": "TAMBILLO"
    },
    "52835141": {
        "Centro Poblado": "TANGAREAL CARRETERA"
    },
    "52835144": {
        "Centro Poblado": "VUELTA CANDELILLA"
    },
    "52835146": {
        "Centro Poblado": "FIRME DE LOS COIMES"
    },
    "52835148": {
        "Centro Poblado": "TABLÓN DULCE LA PAMPA"
    },
    "52835149": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "52835150": {
        "Centro Poblado": "BELLAVISTA"
    },
    "52835151": {
        "Centro Poblado": "VAQUERIA COLOMBIA GRANDE"
    },
    "52835152": {
        "Centro Poblado": "INGUAPI EL GUADUAL"
    },
    "52835153": {
        "Centro Poblado": "CONGAL"
    },
    "52835154": {
        "Centro Poblado": "BAJO GUABAL"
    },
    "52835155": {
        "Centro Poblado": "PEÑA COLORADA"
    },
    "52835156": {
        "Centro Poblado": "BUCHELY"
    },
    "52835157": {
        "Centro Poblado": "CAJAPÍ"
    },
    "52835158": {
        "Centro Poblado": "VARIANTE"
    },
    "52835159": {
        "Centro Poblado": "DOS QUEBRADAS"
    },
    "52835160": {
        "Centro Poblado": "CANDELILLA"
    },
    "52835161": {
        "Centro Poblado": "PIÑAL SALADO"
    },
    "52835162": {
        "Centro Poblado": "CHONTAL"
    },
    "52835163": {
        "Centro Poblado": "IMBILÍ"
    },
    "52835164": {
        "Centro Poblado": "SAN PEDRO DEL VINO"
    },
    "52835166": {
        "Centro Poblado": "SAN SEBASTIÁN"
    },
    "52835167": {
        "Centro Poblado": "BOCA DE TULMO"
    },
    "52835168": {
        "Centro Poblado": "SAGUMBITA"
    },
    "52835174": {
        "Centro Poblado": "LA BRAVA RÍO CAUNAPÍ"
    },
    "52835177": {
        "Centro Poblado": "ACHOTAL"
    },
    "52835178": {
        "Centro Poblado": "AGUACATE"
    },
    "52835179": {
        "Centro Poblado": "ALTO BUENOS AIRES"
    },
    "52835180": {
        "Centro Poblado": "ALTO JAGUA (RÍO MIRA)"
    },
    "52835181": {
        "Centro Poblado": "ALTO SANTO DOMINGO"
    },
    "52835182": {
        "Centro Poblado": "ALTO VILLARICA"
    },
    "52835183": {
        "Centro Poblado": "BAJO BUENOS AIRES (TABLÓN SALADO)"
    },
    "52835184": {
        "Centro Poblado": "BOCAGRANDE"
    },
    "52835185": {
        "Centro Poblado": "BUCHELY 2"
    },
    "52835186": {
        "Centro Poblado": "CAJAPI DEL MIRA"
    },
    "52835187": {
        "Centro Poblado": "CANDELILLAS DE LA MAR"
    },
    "52835188": {
        "Centro Poblado": "CHIMBUZAL"
    },
    "52835190": {
        "Centro Poblado": "GUACHIRI"
    },
    "52835191": {
        "Centro Poblado": "GUADUAL"
    },
    "52835193": {
        "Centro Poblado": "INDA ZABALETA"
    },
    "52835194": {
        "Centro Poblado": "INGUAPI DEL CARMEN 2"
    },
    "52835196": {
        "Centro Poblado": "INGUAPI LA CHIRICANA"
    },
    "52835197": {
        "Centro Poblado": "ISLA GRANDE"
    },
    "52835198": {
        "Centro Poblado": "LA BALSA"
    },
    "52835200": {
        "Centro Poblado": "LA CONCHA (TABLÓN SALADO)"
    },
    "52835201": {
        "Centro Poblado": "13 DE MAYO"
    },
    "52835202": {
        "Centro Poblado": "LAS BRISAS"
    },
    "52835203": {
        "Centro Poblado": "NERETE (RÍO MIRA)"
    },
    "52835204": {
        "Centro Poblado": "NUEVA REFORMA"
    },
    "52835205": {
        "Centro Poblado": "NUEVO PUERTO NIDIA"
    },
    "52835207": {
        "Centro Poblado": "PARAÍSO"
    },
    "52835208": {
        "Centro Poblado": "PIÑAL DULCE"
    },
    "52835209": {
        "Centro Poblado": "PITAL (CHIMBUZAL)"
    },
    "52835210": {
        "Centro Poblado": "PORVENIR"
    },
    "52835211": {
        "Centro Poblado": "PUEBLO NUEVO (RÍO MIRA)"
    },
    "52835212": {
        "Centro Poblado": "PUEBLO NUEVO (TABLÓN SALADO)"
    },
    "52835213": {
        "Centro Poblado": "RESTREPO"
    },
    "52835214": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "52835216": {
        "Centro Poblado": "SAN JUAN PUEBLO NUEVO"
    },
    "52835217": {
        "Centro Poblado": "SAN JUAN (RÍO MIRA)"
    },
    "52835218": {
        "Centro Poblado": "SAN PABLO"
    },
    "52835219": {
        "Centro Poblado": "SAN VICENTE (LAS VARAS)"
    },
    "52835221": {
        "Centro Poblado": "SEIS DE AGOSTO"
    },
    "52835224": {
        "Centro Poblado": "TANGAREAL DEL MIRA"
    },
    "52835226": {
        "Centro Poblado": "VIGUARAL"
    },
    "52835227": {
        "Centro Poblado": "VUELTA CANDELILLAS 2"
    },
    "52835228": {
        "Centro Poblado": "VUELTA DEL CARMEN"
    },
    "52835229": {
        "Centro Poblado": "VUELTA LARGA (RÍO GUANAPI)"
    },
    "52835230": {
        "Centro Poblado": "ZAPOTAL"
    },
    "52835231": {
        "Centro Poblado": "CRISTO REY"
    },
    "52835232": {
        "Centro Poblado": "KILÓMETRO 63"
    },
    "52835233": {
        "Centro Poblado": "KILÓMETRO 75 LA INVASIÓN"
    },
    "52835234": {
        "Centro Poblado": "LA VIÑA"
    },
    "52835235": {
        "Centro Poblado": "VAQUERÍA LA TORRE"
    },
    "52838000": {
        "Centro Poblado": "TÚQUERRES"
    },
    "52838001": {
        "Centro Poblado": "ALBÁN"
    },
    "52838002": {
        "Centro Poblado": "CUATRO ESQUINAS"
    },
    "52838004": {
        "Centro Poblado": "PINZÓN"
    },
    "52838007": {
        "Centro Poblado": "SANTANDER"
    },
    "52838009": {
        "Centro Poblado": "YASCUAL"
    },
    "52838012": {
        "Centro Poblado": "LOS ARRAYANES"
    },
    "52885000": {
        "Centro Poblado": "YACUANQUER"
    },
    "52885006": {
        "Centro Poblado": "MEJÍA"
    },
    "52885007": {
        "Centro Poblado": "LA AGUADA"
    },
    "54001000": {
        "Centro Poblado": "SAN JOSÉ DE CÚCUTA"
    },
    "54001001": {
        "Centro Poblado": "AGUA CLARA"
    },
    "54001002": {
        "Centro Poblado": "BANCO DE ARENAS"
    },
    "54001003": {
        "Centro Poblado": "BUENA ESPERANZA"
    },
    "54001007": {
        "Centro Poblado": "PATILLALES"
    },
    "54001011": {
        "Centro Poblado": "PUERTO VILLAMIZAR"
    },
    "54001015": {
        "Centro Poblado": "RICAURTE"
    },
    "54001017": {
        "Centro Poblado": "SAN FAUSTINO"
    },
    "54001018": {
        "Centro Poblado": "SAN PEDRO"
    },
    "54001025": {
        "Centro Poblado": "ARRAYÁN"
    },
    "54001028": {
        "Centro Poblado": "ALTO VIENTO"
    },
    "54001029": {
        "Centro Poblado": "EL PRADO"
    },
    "54001030": {
        "Centro Poblado": "PÓRTICO"
    },
    "54001033": {
        "Centro Poblado": "LA JARRA"
    },
    "54001036": {
        "Centro Poblado": "PALMARITO"
    },
    "54001038": {
        "Centro Poblado": "PUERTO LEÓN"
    },
    "54001039": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "54001041": {
        "Centro Poblado": "GUARAMITO"
    },
    "54001042": {
        "Centro Poblado": "LA FLORESTA"
    },
    "54001043": {
        "Centro Poblado": "LA PUNTA"
    },
    "54001044": {
        "Centro Poblado": "VIIGILANCIA"
    },
    "54001045": {
        "Centro Poblado": "PUERTO LLERAS"
    },
    "54001046": {
        "Centro Poblado": "SANTA CECILIA"
    },
    "54001047": {
        "Centro Poblado": "CARMEN DE TONCHALÁ"
    },
    "54001049": {
        "Centro Poblado": "ORIPAYA"
    },
    "54001050": {
        "Centro Poblado": "LAS VACAS"
    },
    "54001053": {
        "Centro Poblado": "BELLA VISTA"
    },
    "54001054": {
        "Centro Poblado": "EL PLOMO"
    },
    "54001055": {
        "Centro Poblado": "EL SUSPIRO"
    },
    "54001056": {
        "Centro Poblado": "LA SABANA"
    },
    "54001057": {
        "Centro Poblado": "NUEVO MADRID"
    },
    "54001058": {
        "Centro Poblado": "SAN AGUSTÍN DE LOS POZOS"
    },
    "54001061": {
        "Centro Poblado": "AGUA BLANCA"
    },
    "54001067": {
        "Centro Poblado": "LONDRES"
    },
    "54001068": {
        "Centro Poblado": "BANCO DE ARENAS 2"
    },
    "54003000": {
        "Centro Poblado": "ÁBREGO"
    },
    "54003002": {
        "Centro Poblado": "CASITAS"
    },
    "54051000": {
        "Centro Poblado": "ARBOLEDAS"
    },
    "54051002": {
        "Centro Poblado": "CASTRO"
    },
    "54051005": {
        "Centro Poblado": "VILLA SUCRE"
    },
    "54099000": {
        "Centro Poblado": "BOCHALEMA"
    },
    "54099002": {
        "Centro Poblado": "LA DONJUANA"
    },
    "54099005": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "54109000": {
        "Centro Poblado": "BUCARASICA"
    },
    "54109002": {
        "Centro Poblado": "LA CURVA"
    },
    "54109003": {
        "Centro Poblado": "LA SANJUANA"
    },
    "54125000": {
        "Centro Poblado": "CÁCOTA"
    },
    "54128000": {
        "Centro Poblado": "CÁCHIRA"
    },
    "54128001": {
        "Centro Poblado": "LA CARRERA"
    },
    "54128003": {
        "Centro Poblado": "LA VEGA"
    },
    "54128011": {
        "Centro Poblado": "LOS MANGOS"
    },
    "54128015": {
        "Centro Poblado": "SAN JOSÉ DEL LLANO"
    },
    "54172000": {
        "Centro Poblado": "CHINÁCOTA"
    },
    "54172001": {
        "Centro Poblado": "LA NUEVA DONJUANA"
    },
    "54172005": {
        "Centro Poblado": "EL NUEVO DIAMANTE"
    },
    "54172006": {
        "Centro Poblado": "CHITACOMAR"
    },
    "54172007": {
        "Centro Poblado": "RECTA LOS ALAMOS"
    },
    "54172008": {
        "Centro Poblado": "TENERIA"
    },
    "54174000": {
        "Centro Poblado": "CHITAGÁ"
    },
    "54174002": {
        "Centro Poblado": "SAN LUIS DE CHUCARIMA"
    },
    "54174005": {
        "Centro Poblado": "LLANO GRANDE"
    },
    "54174006": {
        "Centro Poblado": "PRESIDENTE"
    },
    "54206000": {
        "Centro Poblado": "CONVENCIÓN"
    },
    "54206002": {
        "Centro Poblado": "CARTAGENITA"
    },
    "54206004": {
        "Centro Poblado": "EL GUAMAL"
    },
    "54206005": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "54206011": {
        "Centro Poblado": "LA LIBERTAD"
    },
    "54206012": {
        "Centro Poblado": "LA VEGA"
    },
    "54206013": {
        "Centro Poblado": "PIEDECUESTA"
    },
    "54206015": {
        "Centro Poblado": "LA TRINIDAD"
    },
    "54206016": {
        "Centro Poblado": "MIRAFLORES"
    },
    "54223000": {
        "Centro Poblado": "CUCUTILLA"
    },
    "54223002": {
        "Centro Poblado": "SAN JOSÉ DE LA MONTAÑA"
    },
    "54223004": {
        "Centro Poblado": "TIERRA GRATA"
    },
    "54239000": {
        "Centro Poblado": "DURANIA"
    },
    "54239002": {
        "Centro Poblado": "HATOVIEJO"
    },
    "54239003": {
        "Centro Poblado": "LA CUCHILLA"
    },
    "54239004": {
        "Centro Poblado": "LA MONTUOSA"
    },
    "54239007": {
        "Centro Poblado": "LAS AGUADAS"
    },
    "54245000": {
        "Centro Poblado": "EL CARMEN"
    },
    "54245006": {
        "Centro Poblado": "GUAMALITO"
    },
    "54250000": {
        "Centro Poblado": "EL TARRA"
    },
    "54250002": {
        "Centro Poblado": "ORÚ"
    },
    "54250003": {
        "Centro Poblado": "FILO GRINGO"
    },
    "54250005": {
        "Centro Poblado": "EL PASO"
    },
    "54250007": {
        "Centro Poblado": "LA CAMPANA"
    },
    "54261000": {
        "Centro Poblado": "EL ZULIA"
    },
    "54261006": {
        "Centro Poblado": "LAS PIEDRAS"
    },
    "54261007": {
        "Centro Poblado": "ASTILLEROS LA YE"
    },
    "54261008": {
        "Centro Poblado": "CAMILANDIA"
    },
    "54261009": {
        "Centro Poblado": "CRISTO REY"
    },
    "54261010": {
        "Centro Poblado": "EL TABLAZO"
    },
    "54261011": {
        "Centro Poblado": "LAS BRISAS"
    },
    "54261012": {
        "Centro Poblado": "SANTA ROSA"
    },
    "54261013": {
        "Centro Poblado": "7 DE AGOSTO"
    },
    "54313000": {
        "Centro Poblado": "GRAMALOTE"
    },
    "54313005": {
        "Centro Poblado": "LA LOMITA"
    },
    "54313006": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "54313007": {
        "Centro Poblado": "POMARROSO"
    },
    "54344000": {
        "Centro Poblado": "HACARÍ"
    },
    "54344003": {
        "Centro Poblado": "MARACAIBO"
    },
    "54344008": {
        "Centro Poblado": "SAN JOSÉ DEL TARRA"
    },
    "54344009": {
        "Centro Poblado": "LAS JUNTAS"
    },
    "54344011": {
        "Centro Poblado": "LA ESTACION O MESITAS"
    },
    "54347000": {
        "Centro Poblado": "HERRÁN"
    },
    "54377000": {
        "Centro Poblado": "LABATECA"
    },
    "54385000": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "54385001": {
        "Centro Poblado": "LA PEDREGOSA"
    },
    "54385002": {
        "Centro Poblado": "LEÓN XIII"
    },
    "54385003": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "54385005": {
        "Centro Poblado": "EL TROPEZÓN"
    },
    "54385007": {
        "Centro Poblado": "LOS CEDROS"
    },
    "54385008": {
        "Centro Poblado": "VILLAMARÍA"
    },
    "54385009": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "54385010": {
        "Centro Poblado": "LA CANCHA"
    },
    "54398000": {
        "Centro Poblado": "LA PLAYA"
    },
    "54398002": {
        "Centro Poblado": "ASPÁSICA"
    },
    "54398006": {
        "Centro Poblado": "LA VEGA DE SAN ANTONIO"
    },
    "54405000": {
        "Centro Poblado": "LOS PATIOS"
    },
    "54405001": {
        "Centro Poblado": "LA GARITA"
    },
    "54405003": {
        "Centro Poblado": "LOS VADOS"
    },
    "54405004": {
        "Centro Poblado": "AGUA LINDA"
    },
    "54405006": {
        "Centro Poblado": "EL TRAPICHE"
    },
    "54405007": {
        "Centro Poblado": "COROZAL VEREDA CALIFORNIA"
    },
    "54405008": {
        "Centro Poblado": "LAGOS DE PALUJAN"
    },
    "54405009": {
        "Centro Poblado": "RECTA COROZAL"
    },
    "54405010": {
        "Centro Poblado": "VILLA KATHERINE"
    },
    "54405011": {
        "Centro Poblado": "VILLAS DE COROZAL"
    },
    "54418000": {
        "Centro Poblado": "LOURDES"
    },
    "54480000": {
        "Centro Poblado": "MUTISCUA"
    },
    "54480001": {
        "Centro Poblado": "LA LAGUNA"
    },
    "54480003": {
        "Centro Poblado": "LA CALDERA"
    },
    "54498000": {
        "Centro Poblado": "OCAÑA"
    },
    "54498002": {
        "Centro Poblado": "AGUASCLARAS"
    },
    "54498005": {
        "Centro Poblado": "OTARÉ"
    },
    "54498006": {
        "Centro Poblado": "BUENAVISTA"
    },
    "54498008": {
        "Centro Poblado": "LA ERMITA"
    },
    "54498009": {
        "Centro Poblado": "LA FLORESTA"
    },
    "54498012": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "54498025": {
        "Centro Poblado": "ALGODONAL"
    },
    "54498026": {
        "Centro Poblado": "CLUB ALL STAR"
    },
    "54518000": {
        "Centro Poblado": "PAMPLONA"
    },
    "54520000": {
        "Centro Poblado": "PAMPLONITA"
    },
    "54520001": {
        "Centro Poblado": "EL DIAMANTE"
    },
    "54520002": {
        "Centro Poblado": "EL TREVEJO"
    },
    "54553000": {
        "Centro Poblado": "PUERTO SANTANDER"
    },
    "54553001": {
        "Centro Poblado": "EL DIAMANTE"
    },
    "54599000": {
        "Centro Poblado": "RAGONVALIA"
    },
    "54599005": {
        "Centro Poblado": "CALICHES"
    },
    "54660000": {
        "Centro Poblado": "SALAZAR DE LAS PALMAS"
    },
    "54660001": {
        "Centro Poblado": "EL CARMEN DE NAZARETH"
    },
    "54660002": {
        "Centro Poblado": "LA LAGUNA"
    },
    "54660005": {
        "Centro Poblado": "SAN JOSÉ DEL AVILA"
    },
    "54660007": {
        "Centro Poblado": "EL SALADO"
    },
    "54670000": {
        "Centro Poblado": "SAN CALIXTO"
    },
    "54670004": {
        "Centro Poblado": "VISTA HERMOSA"
    },
    "54670010": {
        "Centro Poblado": "PALMARITO"
    },
    "54670016": {
        "Centro Poblado": "LA QUINA"
    },
    "54670017": {
        "Centro Poblado": "LAGUNITAS"
    },
    "54673000": {
        "Centro Poblado": "SAN CAYETANO"
    },
    "54673002": {
        "Centro Poblado": "CORNEJO"
    },
    "54673005": {
        "Centro Poblado": "URIMACO"
    },
    "54673008": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "54680000": {
        "Centro Poblado": "SANTIAGO"
    },
    "54720000": {
        "Centro Poblado": "SARDINATA"
    },
    "54720002": {
        "Centro Poblado": "EL CARMEN"
    },
    "54720003": {
        "Centro Poblado": "LA VICTORIA"
    },
    "54720004": {
        "Centro Poblado": "LAS MERCEDES"
    },
    "54720005": {
        "Centro Poblado": "LUIS VERO"
    },
    "54720006": {
        "Centro Poblado": "SAN MARTÍN DE LOBA"
    },
    "54720007": {
        "Centro Poblado": "SAN ROQUE"
    },
    "54743000": {
        "Centro Poblado": "SILOS"
    },
    "54743001": {
        "Centro Poblado": "BABEGA"
    },
    "54743003": {
        "Centro Poblado": "LOS RINCÓN"
    },
    "54743004": {
        "Centro Poblado": "LA LAGUNA"
    },
    "54743006": {
        "Centro Poblado": "PACHAGUAL"
    },
    "54800000": {
        "Centro Poblado": "TEORAMA"
    },
    "54800011": {
        "Centro Poblado": "LA CECILIA"
    },
    "54800022": {
        "Centro Poblado": "SAN PABLO"
    },
    "54800025": {
        "Centro Poblado": "QUINCE LETRAS"
    },
    "54800026": {
        "Centro Poblado": "EL ASERRÍO"
    },
    "54810000": {
        "Centro Poblado": "TIBÚ"
    },
    "54810002": {
        "Centro Poblado": "LA GABARRA"
    },
    "54810003": {
        "Centro Poblado": "PACCELLY"
    },
    "54810006": {
        "Centro Poblado": "TRES BOCAS"
    },
    "54810008": {
        "Centro Poblado": "PETRÓLEA"
    },
    "54810009": {
        "Centro Poblado": "VERSALLES"
    },
    "54810011": {
        "Centro Poblado": "CAMPO GILES"
    },
    "54810013": {
        "Centro Poblado": "LA LLANA"
    },
    "54810016": {
        "Centro Poblado": "VETAS DE ORIENTE"
    },
    "54810017": {
        "Centro Poblado": "CAMPO DOS"
    },
    "54810018": {
        "Centro Poblado": "LA CUATRO"
    },
    "54820000": {
        "Centro Poblado": "TOLEDO"
    },
    "54820008": {
        "Centro Poblado": "SAN BERNARDO DE BATA"
    },
    "54820015": {
        "Centro Poblado": "SAMORE"
    },
    "54871000": {
        "Centro Poblado": "VILLA CARO"
    },
    "54874000": {
        "Centro Poblado": "VILLA DEL ROSARIO"
    },
    "54874001": {
        "Centro Poblado": "JUAN FRÍO"
    },
    "54874008": {
        "Centro Poblado": "PALOGORDO NORTE"
    },
    "63001000": {
        "Centro Poblado": "ARMENIA"
    },
    "63001001": {
        "Centro Poblado": "EL CAIMO"
    },
    "63001002": {
        "Centro Poblado": "MURILLO"
    },
    "63001008": {
        "Centro Poblado": "CASERIO SANTA HELENA"
    },
    "63001009": {
        "Centro Poblado": "CONDOMINIO EL EDEN"
    },
    "63001010": {
        "Centro Poblado": "CONDOMINIOS LAS VEGAS, IRAKA Y LAGOS DE IRAKA"
    },
    "63001011": {
        "Centro Poblado": "CONDOMINIO PALO DE AGUA"
    },
    "63001012": {
        "Centro Poblado": "CONDOMINIO PONTEVEDRA"
    },
    "63001013": {
        "Centro Poblado": "CONDOMINIO SENIORS CLUB"
    },
    "63001015": {
        "Centro Poblado": "NUEVO HORIZONTE - SAPERA"
    },
    "63001016": {
        "Centro Poblado": "SECTOR CENEXPO"
    },
    "63111000": {
        "Centro Poblado": "BUENAVISTA"
    },
    "63111001": {
        "Centro Poblado": "RÍO VERDE"
    },
    "63130000": {
        "Centro Poblado": "CALARCÁ"
    },
    "63130001": {
        "Centro Poblado": "BARCELONA"
    },
    "63130003": {
        "Centro Poblado": "LA BELLA"
    },
    "63130004": {
        "Centro Poblado": "LA VIRGINIA"
    },
    "63130005": {
        "Centro Poblado": "QUEBRADANEGRA"
    },
    "63130008": {
        "Centro Poblado": "LA PRADERA"
    },
    "63130010": {
        "Centro Poblado": "LA MARÍA"
    },
    "63130013": {
        "Centro Poblado": "BARRAGÁN"
    },
    "63130015": {
        "Centro Poblado": "CONDOMINIO LOS ALMENDROS"
    },
    "63130016": {
        "Centro Poblado": "CONDOMINIO VALLE DEL SOL"
    },
    "63130018": {
        "Centro Poblado": "CONDOMINIO AGUA BONITA"
    },
    "63130019": {
        "Centro Poblado": "CONDOMINIO LA MICAELA"
    },
    "63190000": {
        "Centro Poblado": "CIRCASIA"
    },
    "63190001": {
        "Centro Poblado": "LA POLA"
    },
    "63190002": {
        "Centro Poblado": "LA SIRIA"
    },
    "63190003": {
        "Centro Poblado": "PIAMONTE"
    },
    "63190004": {
        "Centro Poblado": "SANTA RITA"
    },
    "63190006": {
        "Centro Poblado": "VILLARAZO - SAN LUIS"
    },
    "63190007": {
        "Centro Poblado": "LA JULIA"
    },
    "63190008": {
        "Centro Poblado": "LA FRONTERA"
    },
    "63190009": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "63190010": {
        "Centro Poblado": "EL PLANAZO"
    },
    "63190011": {
        "Centro Poblado": "LA 18 GUAYABAL"
    },
    "63190012": {
        "Centro Poblado": "URBANIZACIÓN EL CANEY"
    },
    "63190013": {
        "Centro Poblado": "CONDOMINIO BOSQUES DE TOSCANA"
    },
    "63190014": {
        "Centro Poblado": "CONDOMINIO LA ALDEA"
    },
    "63190016": {
        "Centro Poblado": "CONDOMINIO LOS ABEDULES Y YARUMOS I"
    },
    "63190017": {
        "Centro Poblado": "CONDOMINIO LOS ROBLES"
    },
    "63190018": {
        "Centro Poblado": "CONDOMINIO LOS ROSALES"
    },
    "63190020": {
        "Centro Poblado": "CONDOMINIO QUINTAS DEL BOSQUE"
    },
    "63190022": {
        "Centro Poblado": "VILLA LIGIA"
    },
    "63190024": {
        "Centro Poblado": "LA CABAÑA"
    },
    "63190028": {
        "Centro Poblado": "CONDOMINIO MONTERREY"
    },
    "63190030": {
        "Centro Poblado": "CONDOMINIO ANGELES DEL BOSQUE"
    },
    "63190031": {
        "Centro Poblado": "CONDOMINIO CEDRO NEGRO"
    },
    "63190032": {
        "Centro Poblado": "CONDOMINIO RESERVAS DEL BOSQUE"
    },
    "63190033": {
        "Centro Poblado": "EL CONGAL"
    },
    "63190034": {
        "Centro Poblado": "LA CRISTALINA"
    },
    "63190035": {
        "Centro Poblado": "HACIENDA HORIZONTES"
    },
    "63212000": {
        "Centro Poblado": "CÓRDOBA"
    },
    "63272000": {
        "Centro Poblado": "FILANDIA"
    },
    "63272002": {
        "Centro Poblado": "LA INDIA"
    },
    "63302000": {
        "Centro Poblado": "GÉNOVA"
    },
    "63401000": {
        "Centro Poblado": "LA TEBAIDA"
    },
    "63401003": {
        "Centro Poblado": "LA SILVIA"
    },
    "63401004": {
        "Centro Poblado": "FUNDACIÓN AMANECER"
    },
    "63401005": {
        "Centro Poblado": "CONDOMINIO LA ESTACIÓN"
    },
    "63401006": {
        "Centro Poblado": "CONDOMINIO MORACAWA"
    },
    "63401007": {
        "Centro Poblado": "MURILLO"
    },
    "63470000": {
        "Centro Poblado": "MONTENEGRO"
    },
    "63470001": {
        "Centro Poblado": "EL CUZCO"
    },
    "63470003": {
        "Centro Poblado": "PUEBLO TAPADO"
    },
    "63470004": {
        "Centro Poblado": "ONCE CASAS"
    },
    "63470007": {
        "Centro Poblado": "EL CASTILLO"
    },
    "63470008": {
        "Centro Poblado": "EL GIGANTE"
    },
    "63470009": {
        "Centro Poblado": "BARAYA"
    },
    "63470010": {
        "Centro Poblado": "LA MONTAÑA"
    },
    "63470013": {
        "Centro Poblado": "CALLE LARGA"
    },
    "63470014": {
        "Centro Poblado": "CONDOMINIO LA HACIENDA"
    },
    "63548000": {
        "Centro Poblado": "PIJAO"
    },
    "63548002": {
        "Centro Poblado": "LA MARIELA"
    },
    "63594000": {
        "Centro Poblado": "QUIMBAYA"
    },
    "63594002": {
        "Centro Poblado": "EL LAUREL"
    },
    "63594003": {
        "Centro Poblado": "LA ESPAÑOLA"
    },
    "63594005": {
        "Centro Poblado": "PUEBLO RICO"
    },
    "63594006": {
        "Centro Poblado": "PUERTO ALEJANDRÍA"
    },
    "63594007": {
        "Centro Poblado": "EL NARANJAL"
    },
    "63594009": {
        "Centro Poblado": "CONDOMINIO CAMPESTRE INCAS PANACA"
    },
    "63690000": {
        "Centro Poblado": "SALENTO"
    },
    "63690001": {
        "Centro Poblado": "BOQUÍA"
    },
    "63690005": {
        "Centro Poblado": "LA EXPLANACIÓN"
    },
    "63690007": {
        "Centro Poblado": "CONDOMINIO LAS COLINAS"
    },
    "63690009": {
        "Centro Poblado": "SAN JUAN DE CAROLINA"
    },
    "63690010": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "63690011": {
        "Centro Poblado": "LOS PINOS"
    },
    "66001000": {
        "Centro Poblado": "PEREIRA"
    },
    "66001001": {
        "Centro Poblado": "ALTAGRACIA"
    },
    "66001002": {
        "Centro Poblado": "ARABIA"
    },
    "66001003": {
        "Centro Poblado": "BETULIA"
    },
    "66001004": {
        "Centro Poblado": "CAIMALITO"
    },
    "66001005": {
        "Centro Poblado": "EL PLACER (COMBIA)"
    },
    "66001006": {
        "Centro Poblado": "LA CONVENCIÓN"
    },
    "66001007": {
        "Centro Poblado": "EL ROCÍO"
    },
    "66001009": {
        "Centro Poblado": "LA BELLA"
    },
    "66001010": {
        "Centro Poblado": "LA FLORIDA"
    },
    "66001013": {
        "Centro Poblado": "LA SELVA"
    },
    "66001015": {
        "Centro Poblado": "MORELIA"
    },
    "66001016": {
        "Centro Poblado": "MUNDO NUEVO"
    },
    "66001018": {
        "Centro Poblado": "PUERTO CALDAS"
    },
    "66001020": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "66001021": {
        "Centro Poblado": "TRIBUNAS CORCEGA"
    },
    "66001025": {
        "Centro Poblado": "NUEVA SIRIA"
    },
    "66001026": {
        "Centro Poblado": "SAN VICENTE"
    },
    "66001028": {
        "Centro Poblado": "YARUMAL"
    },
    "66001029": {
        "Centro Poblado": "LA BANANERA"
    },
    "66001030": {
        "Centro Poblado": "ALTO ALEGRÍAS"
    },
    "66001031": {
        "Centro Poblado": "ALEGRÍAS"
    },
    "66001032": {
        "Centro Poblado": "PÉREZ ALTO"
    },
    "66001035": {
        "Centro Poblado": "HUERTAS"
    },
    "66001036": {
        "Centro Poblado": "PITAL DE COMBIA"
    },
    "66001037": {
        "Centro Poblado": "EL CHOCHO"
    },
    "66001039": {
        "Centro Poblado": "BARRIO EL BOSQUE"
    },
    "66001040": {
        "Centro Poblado": "LA CABAÑITA"
    },
    "66001041": {
        "Centro Poblado": "BELMONTE BAJO"
    },
    "66001043": {
        "Centro Poblado": "BETANIA"
    },
    "66001044": {
        "Centro Poblado": "BRISAS DE CONDINA (LA GRAMÍNEA)"
    },
    "66001045": {
        "Centro Poblado": "CALLE LARGA"
    },
    "66001046": {
        "Centro Poblado": "CARACOL LA CURVA"
    },
    "66001047": {
        "Centro Poblado": "CESTILLAL"
    },
    "66001048": {
        "Centro Poblado": "EL CONTENTO"
    },
    "66001049": {
        "Centro Poblado": "EL CRUCERO DE COMBIA"
    },
    "66001050": {
        "Centro Poblado": "EL JAZMÍN"
    },
    "66001051": {
        "Centro Poblado": "EL MANZANO"
    },
    "66001052": {
        "Centro Poblado": "EL PORVENIR"
    },
    "66001053": {
        "Centro Poblado": "ESPERANZA GALICIA"
    },
    "66001054": {
        "Centro Poblado": "ESTACIÓN AZUFRAL"
    },
    "66001055": {
        "Centro Poblado": "ESTRELLA MORRÓN"
    },
    "66001056": {
        "Centro Poblado": "CONDINA GUACARY"
    },
    "66001057": {
        "Centro Poblado": "LAGUNETA"
    },
    "66001058": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "66001059": {
        "Centro Poblado": "NUEVO SOL"
    },
    "66001060": {
        "Centro Poblado": "PLAN DE VIVIENDA LA UNIÓN"
    },
    "66001061": {
        "Centro Poblado": "PLAN DE VIVIENDA YARUMAL"
    },
    "66001062": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "66001063": {
        "Centro Poblado": "SAN CARLOS"
    },
    "66001064": {
        "Centro Poblado": "YARUMITO"
    },
    "66001065": {
        "Centro Poblado": "PÉNJAMO"
    },
    "66001066": {
        "Centro Poblado": "ALTO ERAZO"
    },
    "66001067": {
        "Centro Poblado": "CANCELES"
    },
    "66001069": {
        "Centro Poblado": "EL CONGOLO"
    },
    "66001070": {
        "Centro Poblado": "EL JARDÍN"
    },
    "66001071": {
        "Centro Poblado": "ESTACIÓN VILLEGAS"
    },
    "66001072": {
        "Centro Poblado": "GALICIA ALTA"
    },
    "66001073": {
        "Centro Poblado": "GILIPINAS"
    },
    "66001074": {
        "Centro Poblado": "HERIBERTO HERRERA"
    },
    "66001075": {
        "Centro Poblado": "LA CARBONERA"
    },
    "66001077": {
        "Centro Poblado": "LA RENTA"
    },
    "66001078": {
        "Centro Poblado": "LA SUIZA"
    },
    "66001079": {
        "Centro Poblado": "LA YE"
    },
    "66001080": {
        "Centro Poblado": "LIBARE"
    },
    "66001081": {
        "Centro Poblado": "PÉREZ BAJO"
    },
    "66001082": {
        "Centro Poblado": "SAN MARINO"
    },
    "66001083": {
        "Centro Poblado": "TRIBUNAS CONSOTA"
    },
    "66001084": {
        "Centro Poblado": "EL JORDÁN"
    },
    "66001085": {
        "Centro Poblado": "SANTANDER"
    },
    "66001089": {
        "Centro Poblado": "CONDOMINIO ANDALUZ"
    },
    "66001090": {
        "Centro Poblado": "CONDOMINIO EL PARAISO"
    },
    "66001091": {
        "Centro Poblado": "CONDOMINIO MACONDO"
    },
    "66001092": {
        "Centro Poblado": "CONDOMINIO MARACAY"
    },
    "66001093": {
        "Centro Poblado": "CONDOMINIO PALMAR"
    },
    "66001094": {
        "Centro Poblado": "GAITAN LA PLAYA"
    },
    "66045000": {
        "Centro Poblado": "APÍA"
    },
    "66045004": {
        "Centro Poblado": "JORDANIA"
    },
    "66045009": {
        "Centro Poblado": "LA MARÍA"
    },
    "66075000": {
        "Centro Poblado": "BALBOA"
    },
    "66075004": {
        "Centro Poblado": "TAMBORES"
    },
    "66075005": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "66075009": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "66088000": {
        "Centro Poblado": "BELÉN DE UMBRÍA"
    },
    "66088002": {
        "Centro Poblado": "COLUMBIA"
    },
    "66088004": {
        "Centro Poblado": "PUENTE UMBRÍA"
    },
    "66088005": {
        "Centro Poblado": "TAPARCAL"
    },
    "66088010": {
        "Centro Poblado": "EL AGUACATE"
    },
    "66088011": {
        "Centro Poblado": "EL CONGO"
    },
    "66170000": {
        "Centro Poblado": "DOSQUEBRADAS"
    },
    "66170001": {
        "Centro Poblado": "ALTO DEL TORO"
    },
    "66170006": {
        "Centro Poblado": "LA UNIÓN"
    },
    "66170008": {
        "Centro Poblado": "AGUAZUL"
    },
    "66170009": {
        "Centro Poblado": "BUENA VISTA"
    },
    "66170010": {
        "Centro Poblado": "COMUNEROS"
    },
    "66170011": {
        "Centro Poblado": "EL ESTANQUILLO"
    },
    "66170014": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "66170017": {
        "Centro Poblado": "LA PLAYITA"
    },
    "66170020": {
        "Centro Poblado": "NARANJALES"
    },
    "66170021": {
        "Centro Poblado": "SANTANA BAJA"
    },
    "66170022": {
        "Centro Poblado": "VILLA CAROLA"
    },
    "66170024": {
        "Centro Poblado": "EL COFRE"
    },
    "66170026": {
        "Centro Poblado": "LA DIVISA PARTE ALTA"
    },
    "66318000": {
        "Centro Poblado": "GUÁTICA"
    },
    "66318002": {
        "Centro Poblado": "SAN CLEMENTE"
    },
    "66318003": {
        "Centro Poblado": "SANTA ANA"
    },
    "66318006": {
        "Centro Poblado": "TRAVESÍAS"
    },
    "66383000": {
        "Centro Poblado": "LA CELIA"
    },
    "66383001": {
        "Centro Poblado": "PATIO BONITO"
    },
    "66400000": {
        "Centro Poblado": "LA VIRGINIA"
    },
    "66400001": {
        "Centro Poblado": "LA PALMA"
    },
    "66440000": {
        "Centro Poblado": "MARSELLA"
    },
    "66440001": {
        "Centro Poblado": "ALTO CAUCA"
    },
    "66440002": {
        "Centro Poblado": "BELTRÁN"
    },
    "66440003": {
        "Centro Poblado": "LA ARGENTINA"
    },
    "66440008": {
        "Centro Poblado": "PLAN DE VIVIENDA EL RAYO"
    },
    "66440009": {
        "Centro Poblado": "ESTACIÓN PEREIRA"
    },
    "66440013": {
        "Centro Poblado": "PLAN DE VIVIENDA TACURRUMBI"
    },
    "66456000": {
        "Centro Poblado": "MISTRATÓ"
    },
    "66456002": {
        "Centro Poblado": "PUERTO DE ORO"
    },
    "66456003": {
        "Centro Poblado": "SAN ANTONIO DEL CHAMI"
    },
    "66456005": {
        "Centro Poblado": "ALTO PUEBLO RICO"
    },
    "66456008": {
        "Centro Poblado": "MAMPAY"
    },
    "66456010": {
        "Centro Poblado": "PINAR DEL RÍO"
    },
    "66456011": {
        "Centro Poblado": "QUEBRADA ARRIBA"
    },
    "66456012": {
        "Centro Poblado": "RÍO MISTRATO"
    },
    "66572000": {
        "Centro Poblado": "PUEBLO RICO"
    },
    "66572001": {
        "Centro Poblado": "SANTA CECILIA"
    },
    "66572002": {
        "Centro Poblado": "VILLA CLARET"
    },
    "66594000": {
        "Centro Poblado": "QUINCHÍA"
    },
    "66594001": {
        "Centro Poblado": "BATERO"
    },
    "66594002": {
        "Centro Poblado": "IRRA"
    },
    "66594006": {
        "Centro Poblado": "NARANJAL"
    },
    "66594007": {
        "Centro Poblado": "SANTA ELENA"
    },
    "66594012": {
        "Centro Poblado": "MORETA"
    },
    "66594014": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "66594019": {
        "Centro Poblado": "VILLA RICA"
    },
    "66682000": {
        "Centro Poblado": "SANTA ROSA DE CABAL"
    },
    "66682003": {
        "Centro Poblado": "EL ESPAÑOL"
    },
    "66682006": {
        "Centro Poblado": "GUACAS"
    },
    "66682008": {
        "Centro Poblado": "LA CAPILLA"
    },
    "66682009": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "66682010": {
        "Centro Poblado": "LAS MANGAS"
    },
    "66682012": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "66682016": {
        "Centro Poblado": "GUAIMARAL"
    },
    "66682017": {
        "Centro Poblado": "EL LEMBO"
    },
    "66682019": {
        "Centro Poblado": "BAJO SAMARIA"
    },
    "66682020": {
        "Centro Poblado": "LA FLORIDA"
    },
    "66682022": {
        "Centro Poblado": "EL JAZMÍN"
    },
    "66682024": {
        "Centro Poblado": "LA LEONA"
    },
    "66682025": {
        "Centro Poblado": "SAN JUANITO"
    },
    "66687000": {
        "Centro Poblado": "SANTUARIO"
    },
    "66687002": {
        "Centro Poblado": "LA MARINA"
    },
    "66687003": {
        "Centro Poblado": "PERALONSO"
    },
    "66687014": {
        "Centro Poblado": "PLAYA RICA"
    },
    "66687015": {
        "Centro Poblado": "EL ROSAL"
    },
    "68001000": {
        "Centro Poblado": "BUCARAMANGA"
    },
    "68001015": {
        "Centro Poblado": "EL NOGAL"
    },
    "68001016": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "68001017": {
        "Centro Poblado": "VIJAGUAL"
    },
    "68001018": {
        "Centro Poblado": "VILLA CARMELO"
    },
    "68001019": {
        "Centro Poblado": "VILLA LUZ"
    },
    "68013000": {
        "Centro Poblado": "AGUADA"
    },
    "68020000": {
        "Centro Poblado": "ALBANIA"
    },
    "68020001": {
        "Centro Poblado": "CARRETERO"
    },
    "68020002": {
        "Centro Poblado": "EL HATILLO"
    },
    "68020003": {
        "Centro Poblado": "LA MESA"
    },
    "68051000": {
        "Centro Poblado": "ARATOCA"
    },
    "68051001": {
        "Centro Poblado": "CHIFLAS"
    },
    "68051012": {
        "Centro Poblado": "EL HOYO"
    },
    "68051013": {
        "Centro Poblado": "BRISAS DEL CHICAMOCHA"
    },
    "68077000": {
        "Centro Poblado": "BARBOSA"
    },
    "68077001": {
        "Centro Poblado": "CITE"
    },
    "68077003": {
        "Centro Poblado": "BUENAVISTA"
    },
    "68077005": {
        "Centro Poblado": "CRISTALES"
    },
    "68077006": {
        "Centro Poblado": "FRANCISCO DE PAULA"
    },
    "68079000": {
        "Centro Poblado": "BARICHARA"
    },
    "68079001": {
        "Centro Poblado": "GUANE"
    },
    "68081000": {
        "Centro Poblado": "BARRANCABERMEJA, DISTRITO ESPECIAL, PORTUARIO, BIODIVERSO, INDUSTRIAL Y TURÍSTICO"
    },
    "68081001": {
        "Centro Poblado": "EL CENTRO"
    },
    "68081002": {
        "Centro Poblado": "EL LLANITO"
    },
    "68081004": {
        "Centro Poblado": "MESETA SAN RAFAEL"
    },
    "68081006": {
        "Centro Poblado": "SAN RAFAEL DE CHUCURÍ"
    },
    "68081009": {
        "Centro Poblado": "LOS LAURELES"
    },
    "68081010": {
        "Centro Poblado": "LA FORTUNA"
    },
    "68081012": {
        "Centro Poblado": "CAMPO 16"
    },
    "68081013": {
        "Centro Poblado": "CAMPO 23"
    },
    "68081015": {
        "Centro Poblado": "CAMPO 6"
    },
    "68081016": {
        "Centro Poblado": "CAMPO GALÁN"
    },
    "68081018": {
        "Centro Poblado": "CIENAGA DE OPON"
    },
    "68081020": {
        "Centro Poblado": "CRETACEO"
    },
    "68081023": {
        "Centro Poblado": "GALÁN BERLÍN"
    },
    "68081027": {
        "Centro Poblado": "LA FOREST"
    },
    "68081031": {
        "Centro Poblado": "PROGRESO"
    },
    "68081032": {
        "Centro Poblado": "PUEBLO REGAO"
    },
    "68081034": {
        "Centro Poblado": "QUEMADERO"
    },
    "68081036": {
        "Centro Poblado": "EL PALMAR"
    },
    "68092000": {
        "Centro Poblado": "BETULIA"
    },
    "68092008": {
        "Centro Poblado": "TIENDA NUEVA"
    },
    "68092010": {
        "Centro Poblado": "LA PLAYA"
    },
    "68092012": {
        "Centro Poblado": "EL PEAJE"
    },
    "68101000": {
        "Centro Poblado": "BOLÍVAR"
    },
    "68101002": {
        "Centro Poblado": "BERBEO"
    },
    "68101007": {
        "Centro Poblado": "FLÓREZ"
    },
    "68101010": {
        "Centro Poblado": "SANTA ROSA"
    },
    "68101012": {
        "Centro Poblado": "TRAPAL"
    },
    "68101014": {
        "Centro Poblado": "LA HERMOSURA"
    },
    "68101015": {
        "Centro Poblado": "LA MELONA"
    },
    "68101016": {
        "Centro Poblado": "GALLEGOS"
    },
    "68101025": {
        "Centro Poblado": "SAN MARCOS"
    },
    "68121000": {
        "Centro Poblado": "CABRERA"
    },
    "68132000": {
        "Centro Poblado": "CALIFORNIA"
    },
    "68132002": {
        "Centro Poblado": "LA BAJA"
    },
    "68147000": {
        "Centro Poblado": "CAPITANEJO"
    },
    "68152000": {
        "Centro Poblado": "CARCASÍ"
    },
    "68152001": {
        "Centro Poblado": "EL TOBAL"
    },
    "68160000": {
        "Centro Poblado": "CEPITÁ"
    },
    "68162000": {
        "Centro Poblado": "CERRITO"
    },
    "68162007": {
        "Centro Poblado": "SERVITÁ"
    },
    "68167000": {
        "Centro Poblado": "CHARALÁ"
    },
    "68167003": {
        "Centro Poblado": "RIACHUELO"
    },
    "68167005": {
        "Centro Poblado": "VIROLÍN"
    },
    "68169000": {
        "Centro Poblado": "CHARTA"
    },
    "68176000": {
        "Centro Poblado": "CHIMA"
    },
    "68179000": {
        "Centro Poblado": "CHIPATÁ"
    },
    "68179010": {
        "Centro Poblado": "PUENTE GRANDE"
    },
    "68190000": {
        "Centro Poblado": "CIMITARRA"
    },
    "68190002": {
        "Centro Poblado": "PUERTO ARAUJO"
    },
    "68190003": {
        "Centro Poblado": "PUERTO OLAYA"
    },
    "68190004": {
        "Centro Poblado": "ZAMBITO"
    },
    "68190005": {
        "Centro Poblado": "DOS HERMANOS"
    },
    "68190006": {
        "Centro Poblado": "SANTA ROSA"
    },
    "68190009": {
        "Centro Poblado": "LA VERDE"
    },
    "68190010": {
        "Centro Poblado": "GUAYABITO BAJO"
    },
    "68190012": {
        "Centro Poblado": "CAMPO SECO"
    },
    "68190014": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "68190018": {
        "Centro Poblado": "EL ATERRADO"
    },
    "68190019": {
        "Centro Poblado": "LA CARRILERA - KM 28"
    },
    "68190021": {
        "Centro Poblado": "PALMAS DEL GUAYABITO"
    },
    "68190022": {
        "Centro Poblado": "PRIMAVERA"
    },
    "68190023": {
        "Centro Poblado": "SAN JUAN DE LA CARRETERA"
    },
    "68190024": {
        "Centro Poblado": "SAN PEDRO DE LA PAZ"
    },
    "68190025": {
        "Centro Poblado": "CAMPO PADILLA"
    },
    "68190028": {
        "Centro Poblado": "CASCAJERO"
    },
    "68190030": {
        "Centro Poblado": "LA TRAVIATA"
    },
    "68190032": {
        "Centro Poblado": "LA YE DE LA TORRE"
    },
    "68207000": {
        "Centro Poblado": "CONCEPCIÓN"
    },
    "68209000": {
        "Centro Poblado": "CONFINES"
    },
    "68211000": {
        "Centro Poblado": "CONTRATACIÓN"
    },
    "68211001": {
        "Centro Poblado": "SAN PABLO"
    },
    "68217000": {
        "Centro Poblado": "COROMORO"
    },
    "68217001": {
        "Centro Poblado": "CINCELADA"
    },
    "68229000": {
        "Centro Poblado": "CURITÍ"
    },
    "68235000": {
        "Centro Poblado": "EL CARMEN DE CHUCURÍ"
    },
    "68235001": {
        "Centro Poblado": "ANGOSTURAS DE LOS ANDES"
    },
    "68235004": {
        "Centro Poblado": "EL CENTENARIO"
    },
    "68235009": {
        "Centro Poblado": "SANTO DOMINGO DEL RAMO"
    },
    "68235017": {
        "Centro Poblado": "LA EXPLANACIÓN"
    },
    "68235022": {
        "Centro Poblado": "EL 27"
    },
    "68245000": {
        "Centro Poblado": "EL GUACAMAYO"
    },
    "68245003": {
        "Centro Poblado": "SANTA RITA"
    },
    "68250000": {
        "Centro Poblado": "EL PEÑÓN"
    },
    "68250002": {
        "Centro Poblado": "CRUCES"
    },
    "68250003": {
        "Centro Poblado": "OTOVAL - RÍO BLANCO"
    },
    "68250006": {
        "Centro Poblado": "EL GODO"
    },
    "68250007": {
        "Centro Poblado": "GIRÓN"
    },
    "68250009": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "68255000": {
        "Centro Poblado": "EL PLAYÓN"
    },
    "68255001": {
        "Centro Poblado": "BARRIO NUEVO"
    },
    "68255002": {
        "Centro Poblado": "BETANIA"
    },
    "68255007": {
        "Centro Poblado": "ESTACIÓN LAGUNA"
    },
    "68255014": {
        "Centro Poblado": "SAN PEDRO DE TIGRA"
    },
    "68264000": {
        "Centro Poblado": "ENCINO"
    },
    "68266000": {
        "Centro Poblado": "ENCISO"
    },
    "68266002": {
        "Centro Poblado": "PEÑA COLORADA"
    },
    "68271000": {
        "Centro Poblado": "FLORIÁN"
    },
    "68271001": {
        "Centro Poblado": "LA VENTA"
    },
    "68271003": {
        "Centro Poblado": "SAN ANTONIO DE LEONES"
    },
    "68276000": {
        "Centro Poblado": "FLORIDABLANCA"
    },
    "68276011": {
        "Centro Poblado": "EL MORTIÑO"
    },
    "68276012": {
        "Centro Poblado": "MONTEARROYO CONDOMINIO"
    },
    "68276013": {
        "Centro Poblado": "RUITOQUE COUNTRY CLUB CONDOMINIO"
    },
    "68276014": {
        "Centro Poblado": "VALLE DE RUITOQUE"
    },
    "68276016": {
        "Centro Poblado": "VILLAS DE GUADALQUIVIR"
    },
    "68276018": {
        "Centro Poblado": "ALTOS DE ORIENTE"
    },
    "68276019": {
        "Centro Poblado": "BELLAVISTA"
    },
    "68276020": {
        "Centro Poblado": "KM 14"
    },
    "68276021": {
        "Centro Poblado": "LA CIDRA"
    },
    "68276022": {
        "Centro Poblado": "TRINITARIOS"
    },
    "68276023": {
        "Centro Poblado": "CALATRAVA"
    },
    "68296000": {
        "Centro Poblado": "GALÁN"
    },
    "68298000": {
        "Centro Poblado": "GÁMBITA"
    },
    "68298002": {
        "Centro Poblado": "LA PALMA"
    },
    "68307000": {
        "Centro Poblado": "GIRÓN"
    },
    "68307002": {
        "Centro Poblado": "BOCAS"
    },
    "68307003": {
        "Centro Poblado": "MARTA"
    },
    "68307007": {
        "Centro Poblado": "ACAPULCO"
    },
    "68307011": {
        "Centro Poblado": "BARBOSA"
    },
    "68307018": {
        "Centro Poblado": "CHOCOITA"
    },
    "68307020": {
        "Centro Poblado": "EL LAGUITO"
    },
    "68307021": {
        "Centro Poblado": "PUEBLITO VIEJO"
    },
    "68307022": {
        "Centro Poblado": "RIO DE ORO"
    },
    "68307023": {
        "Centro Poblado": "LLANADAS"
    },
    "68307024": {
        "Centro Poblado": "VIENTOS DE LLANADA"
    },
    "68318000": {
        "Centro Poblado": "GUACA"
    },
    "68318001": {
        "Centro Poblado": "BARAYA"
    },
    "68320000": {
        "Centro Poblado": "GUADALUPE"
    },
    "68320005": {
        "Centro Poblado": "EL TIRANO"
    },
    "68322000": {
        "Centro Poblado": "GUAPOTÁ"
    },
    "68324000": {
        "Centro Poblado": "GUAVATÁ"
    },
    "68327000": {
        "Centro Poblado": "GÜEPSA"
    },
    "68344000": {
        "Centro Poblado": "HATO"
    },
    "68368000": {
        "Centro Poblado": "JESÚS MARÍA"
    },
    "68370000": {
        "Centro Poblado": "JORDÁN SUBE"
    },
    "68377000": {
        "Centro Poblado": "LA BELLEZA"
    },
    "68377001": {
        "Centro Poblado": "LA QUITAZ"
    },
    "68377003": {
        "Centro Poblado": "EL RUBÍ"
    },
    "68377005": {
        "Centro Poblado": "LOS VALLES"
    },
    "68385000": {
        "Centro Poblado": "LANDÁZURI"
    },
    "68385001": {
        "Centro Poblado": "BAJO JORDÁN"
    },
    "68385005": {
        "Centro Poblado": "PLAN DE ARMAS"
    },
    "68385006": {
        "Centro Poblado": "SAN IGNACIO DEL OPÓN"
    },
    "68385007": {
        "Centro Poblado": "MIRALINDO"
    },
    "68385008": {
        "Centro Poblado": "KILÓMETRO 15"
    },
    "68385009": {
        "Centro Poblado": "LA INDIA"
    },
    "68385014": {
        "Centro Poblado": "RÍO BLANCO"
    },
    "68397000": {
        "Centro Poblado": "LA PAZ"
    },
    "68397001": {
        "Centro Poblado": "EL HATO"
    },
    "68397002": {
        "Centro Poblado": "LA LOMA"
    },
    "68397005": {
        "Centro Poblado": "TROCHAL"
    },
    "68406000": {
        "Centro Poblado": "LEBRIJA"
    },
    "68406003": {
        "Centro Poblado": "EL CONCHAL"
    },
    "68406009": {
        "Centro Poblado": "PORTUGAL"
    },
    "68406013": {
        "Centro Poblado": "URIBE URIBE"
    },
    "68406014": {
        "Centro Poblado": "VANEGAS"
    },
    "68406026": {
        "Centro Poblado": "CONDOMINIO VILLAS DE PALO NEGRO"
    },
    "68418000": {
        "Centro Poblado": "LOS SANTOS"
    },
    "68418006": {
        "Centro Poblado": "MAJADAL ALTO"
    },
    "68425000": {
        "Centro Poblado": "MACARAVITA"
    },
    "68425003": {
        "Centro Poblado": "LA BRICHA"
    },
    "68432000": {
        "Centro Poblado": "MÁLAGA"
    },
    "68432009": {
        "Centro Poblado": "ASODEMA"
    },
    "68444000": {
        "Centro Poblado": "MATANZA"
    },
    "68444006": {
        "Centro Poblado": "SANTA CRUZ DE LA COLINA"
    },
    "68464000": {
        "Centro Poblado": "MOGOTES"
    },
    "68464002": {
        "Centro Poblado": "PITIGUAO"
    },
    "68464016": {
        "Centro Poblado": "LOS CAUCHOS"
    },
    "68468000": {
        "Centro Poblado": "MOLAGAVITA"
    },
    "68468002": {
        "Centro Poblado": "EL JUNCO"
    },
    "68498000": {
        "Centro Poblado": "OCAMONTE"
    },
    "68500000": {
        "Centro Poblado": "OIBA"
    },
    "68500006": {
        "Centro Poblado": "PUENTE LLANO"
    },
    "68502000": {
        "Centro Poblado": "ONZAGA"
    },
    "68502001": {
        "Centro Poblado": "PADUA"
    },
    "68502002": {
        "Centro Poblado": "SUSA"
    },
    "68502004": {
        "Centro Poblado": "EL CARMEN"
    },
    "68522000": {
        "Centro Poblado": "PALMAR"
    },
    "68524000": {
        "Centro Poblado": "PALMAS DEL SOCORRO"
    },
    "68533000": {
        "Centro Poblado": "PÁRAMO"
    },
    "68547000": {
        "Centro Poblado": "PIEDECUESTA"
    },
    "68547003": {
        "Centro Poblado": "SEVILLA"
    },
    "68547007": {
        "Centro Poblado": "UMPALÁ"
    },
    "68547008": {
        "Centro Poblado": "PESCADERO"
    },
    "68547010": {
        "Centro Poblado": "LA COLINA"
    },
    "68547011": {
        "Centro Poblado": "LOS CUROS"
    },
    "68547016": {
        "Centro Poblado": "CONDOMINIO RUITOQUE COUNTRY CLUB"
    },
    "68547017": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "68547018": {
        "Centro Poblado": "BUENOS AIRES MESA RUITOQUE"
    },
    "68547019": {
        "Centro Poblado": "LA VEGA"
    },
    "68547020": {
        "Centro Poblado": "LA DIVA"
    },
    "68547021": {
        "Centro Poblado": "ALTAMIRA"
    },
    "68547022": {
        "Centro Poblado": "CAMPO CAMPIÑA"
    },
    "68547023": {
        "Centro Poblado": "CIUDAD TEYUNA"
    },
    "68547024": {
        "Centro Poblado": "EDEN"
    },
    "68547025": {
        "Centro Poblado": "MIRADOR DEL LAGO"
    },
    "68547026": {
        "Centro Poblado": "NUEVA COLOMBIA"
    },
    "68547028": {
        "Centro Poblado": "PARAMITO"
    },
    "68549000": {
        "Centro Poblado": "PINCHOTE"
    },
    "68549003": {
        "Centro Poblado": "BARRIO PORTAL DEL CONDE"
    },
    "68572000": {
        "Centro Poblado": "PUENTE NACIONAL"
    },
    "68572002": {
        "Centro Poblado": "CAPILLA"
    },
    "68572003": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "68572004": {
        "Centro Poblado": "QUEBRADA NEGRA"
    },
    "68572012": {
        "Centro Poblado": "PEÑA BLANCA"
    },
    "68573000": {
        "Centro Poblado": "PUERTO PARRA"
    },
    "68573001": {
        "Centro Poblado": "CAMPO CAPOTE"
    },
    "68573002": {
        "Centro Poblado": "LAS MONTOYAS"
    },
    "68573003": {
        "Centro Poblado": "BOCAS DE CARARE O CARARE VIEJO"
    },
    "68573005": {
        "Centro Poblado": "EL CRUCE"
    },
    "68575000": {
        "Centro Poblado": "PUERTO WILCHES"
    },
    "68575001": {
        "Centro Poblado": "BADILLO"
    },
    "68575003": {
        "Centro Poblado": "BOCAS ROSARIO"
    },
    "68575004": {
        "Centro Poblado": "CARPINTERO"
    },
    "68575005": {
        "Centro Poblado": "CHINGALE"
    },
    "68575006": {
        "Centro Poblado": "EL GUAYABO"
    },
    "68575007": {
        "Centro Poblado": "EL PEDRAL"
    },
    "68575011": {
        "Centro Poblado": "KILOMETRO 20 - COMUNEROS"
    },
    "68575013": {
        "Centro Poblado": "PATURIA"
    },
    "68575014": {
        "Centro Poblado": "PRADILLA"
    },
    "68575015": {
        "Centro Poblado": "PUENTE SOGAMOSO"
    },
    "68575018": {
        "Centro Poblado": "VIJAGUAL"
    },
    "68575019": {
        "Centro Poblado": "PUERTO CAYUMBA"
    },
    "68575022": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "68575023": {
        "Centro Poblado": "KILÓMETRO OCHO"
    },
    "68575024": {
        "Centro Poblado": "SAN CLAVER"
    },
    "68575025": {
        "Centro Poblado": "GARCÍA CADENA"
    },
    "68575026": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "68575027": {
        "Centro Poblado": "CAMPO DURO"
    },
    "68575028": {
        "Centro Poblado": "CURUMITA"
    },
    "68575029": {
        "Centro Poblado": "SANTA TERESA"
    },
    "68575030": {
        "Centro Poblado": "TALADRO II"
    },
    "68575031": {
        "Centro Poblado": "INVASIÓN LA INDEPENDENCIA"
    },
    "68615000": {
        "Centro Poblado": "RIONEGRO"
    },
    "68615002": {
        "Centro Poblado": "CUESTA RICA"
    },
    "68615009": {
        "Centro Poblado": "LA CEIBA"
    },
    "68615011": {
        "Centro Poblado": "LLANO DE PALMAS"
    },
    "68615012": {
        "Centro Poblado": "MISIJUAY"
    },
    "68615013": {
        "Centro Poblado": "PAPAYAL"
    },
    "68615017": {
        "Centro Poblado": "VEINTE DE JULIO"
    },
    "68615027": {
        "Centro Poblado": "LOS CHORROS (SAN JOSÉ)"
    },
    "68615031": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "68615036": {
        "Centro Poblado": "EL BAMBÚ"
    },
    "68655000": {
        "Centro Poblado": "SABANA DE TORRES"
    },
    "68655001": {
        "Centro Poblado": "LA GÓMEZ"
    },
    "68655002": {
        "Centro Poblado": "SABANETA"
    },
    "68655004": {
        "Centro Poblado": "PROVINCIA"
    },
    "68655006": {
        "Centro Poblado": "VERACRUZ KILÓMETRO 80"
    },
    "68655007": {
        "Centro Poblado": "SAN LUIS DE MAGARA"
    },
    "68655008": {
        "Centro Poblado": "PAYOA CINCO"
    },
    "68655009": {
        "Centro Poblado": "PUERTO SANTOS"
    },
    "68655011": {
        "Centro Poblado": "CERRITO"
    },
    "68655013": {
        "Centro Poblado": "KILÓMETRO 36"
    },
    "68655014": {
        "Centro Poblado": "LA PAMPA"
    },
    "68655015": {
        "Centro Poblado": "SAN LUIS DE RIO SUCIO"
    },
    "68669000": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "68669005": {
        "Centro Poblado": "LAGUNA DE ORTICES"
    },
    "68669007": {
        "Centro Poblado": "PANGOTE"
    },
    "68673000": {
        "Centro Poblado": "SAN BENITO"
    },
    "68673003": {
        "Centro Poblado": "SAN BENITO NUEVO"
    },
    "68673004": {
        "Centro Poblado": "LA CARRERA"
    },
    "68673005": {
        "Centro Poblado": "LAS CASITAS"
    },
    "68679000": {
        "Centro Poblado": "SAN GIL"
    },
    "68682000": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "68682001": {
        "Centro Poblado": "RICAURTE"
    },
    "68684000": {
        "Centro Poblado": "SAN JOSÉ DE MIRANDA"
    },
    "68684009": {
        "Centro Poblado": "VILLA JARDÍN"
    },
    "68686000": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "68689000": {
        "Centro Poblado": "SAN VICENTE DE CHUCURÍ"
    },
    "68689001": {
        "Centro Poblado": "ALBANIA"
    },
    "68689012": {
        "Centro Poblado": "YARIMA"
    },
    "68689028": {
        "Centro Poblado": "LAS ACACIAS"
    },
    "68705000": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "68720000": {
        "Centro Poblado": "SANTA HELENA DEL OPÓN"
    },
    "68720001": {
        "Centro Poblado": "LA ARAGUA"
    },
    "68720002": {
        "Centro Poblado": "CACHIPAY"
    },
    "68720004": {
        "Centro Poblado": "PLAN DE ALVAREZ"
    },
    "68720005": {
        "Centro Poblado": "SAN JUAN BOSCO DE LA VERDE"
    },
    "68745000": {
        "Centro Poblado": "SIMACOTA"
    },
    "68745006": {
        "Centro Poblado": "LA LLANITA"
    },
    "68745009": {
        "Centro Poblado": "LA ROCHELA"
    },
    "68745011": {
        "Centro Poblado": "EL GUAMO"
    },
    "68745012": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "68755000": {
        "Centro Poblado": "SOCORRO"
    },
    "68755002": {
        "Centro Poblado": "BERLÍN"
    },
    "68770000": {
        "Centro Poblado": "SUAITA"
    },
    "68770001": {
        "Centro Poblado": "OLIVAL"
    },
    "68770002": {
        "Centro Poblado": "SAN JOSÉ DE SUAITA"
    },
    "68770003": {
        "Centro Poblado": "VADO REAL"
    },
    "68770008": {
        "Centro Poblado": "TOLOTÁ"
    },
    "68773000": {
        "Centro Poblado": "SUCRE"
    },
    "68773001": {
        "Centro Poblado": "LA GRANJA"
    },
    "68773002": {
        "Centro Poblado": "LA PRADERA"
    },
    "68773003": {
        "Centro Poblado": "SABANA GRANDE"
    },
    "68773014": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "68773015": {
        "Centro Poblado": "EL LÍBANO"
    },
    "68780000": {
        "Centro Poblado": "SURATÁ"
    },
    "68780001": {
        "Centro Poblado": "CACHIRÍ"
    },
    "68780008": {
        "Centro Poblado": "TURBAY"
    },
    "68820000": {
        "Centro Poblado": "TONA"
    },
    "68820001": {
        "Centro Poblado": "BERLÍN"
    },
    "68820002": {
        "Centro Poblado": "LA CORCOVA"
    },
    "68820007": {
        "Centro Poblado": "VILLAVERDE"
    },
    "68855000": {
        "Centro Poblado": "VALLE DE SAN JOSÉ"
    },
    "68861000": {
        "Centro Poblado": "VÉLEZ"
    },
    "68861001": {
        "Centro Poblado": "ALTO JORDÁN"
    },
    "68861002": {
        "Centro Poblado": "GUALILO"
    },
    "68861017": {
        "Centro Poblado": "EL LIMÓN"
    },
    "68861022": {
        "Centro Poblado": "LOMALTA"
    },
    "68861024": {
        "Centro Poblado": "LOS GUAYABOS"
    },
    "68861025": {
        "Centro Poblado": "LA VICINIA"
    },
    "68861026": {
        "Centro Poblado": "PENA BLANCA"
    },
    "68867000": {
        "Centro Poblado": "VETAS"
    },
    "68872000": {
        "Centro Poblado": "VILLANUEVA"
    },
    "68895000": {
        "Centro Poblado": "ZAPATOCA"
    },
    "68895001": {
        "Centro Poblado": "LA FUENTE"
    },
    "70001000": {
        "Centro Poblado": "SINCELEJO"
    },
    "70001001": {
        "Centro Poblado": "BUENAVISTA"
    },
    "70001002": {
        "Centro Poblado": "CRUZ DEL BEQUE"
    },
    "70001003": {
        "Centro Poblado": "CHOCHO"
    },
    "70001004": {
        "Centro Poblado": "CERRITO DE LA PALMA"
    },
    "70001005": {
        "Centro Poblado": "LA ARENA"
    },
    "70001006": {
        "Centro Poblado": "LA CHIVERA"
    },
    "70001007": {
        "Centro Poblado": "LA GALLERA"
    },
    "70001009": {
        "Centro Poblado": "LAGUNA FLOR"
    },
    "70001011": {
        "Centro Poblado": "LAS MAJAGUAS"
    },
    "70001013": {
        "Centro Poblado": "SABANAS DEL POTRERO"
    },
    "70001014": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "70001015": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "70001016": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "70001017": {
        "Centro Poblado": "BUENAVISTICA"
    },
    "70001020": {
        "Centro Poblado": "POLICARPA"
    },
    "70001021": {
        "Centro Poblado": "SAN JACINTO"
    },
    "70001022": {
        "Centro Poblado": "SAN NICOLAS"
    },
    "70001023": {
        "Centro Poblado": "VILLA ROSITA"
    },
    "70001027": {
        "Centro Poblado": "CERRO DEL NARANJO"
    },
    "70110000": {
        "Centro Poblado": "BUENAVISTA"
    },
    "70110004": {
        "Centro Poblado": "LAS CHICHAS"
    },
    "70110005": {
        "Centro Poblado": "LOS ANONES"
    },
    "70110006": {
        "Centro Poblado": "PROVIDENCIA"
    },
    "70110007": {
        "Centro Poblado": "COSTA RICA"
    },
    "70124000": {
        "Centro Poblado": "CAIMITO"
    },
    "70124001": {
        "Centro Poblado": "EL MAMÓN"
    },
    "70124002": {
        "Centro Poblado": "SIETE PALMAS"
    },
    "70124004": {
        "Centro Poblado": "LOS CAYITOS"
    },
    "70124006": {
        "Centro Poblado": "LA SOLERA"
    },
    "70124007": {
        "Centro Poblado": "TOFEME"
    },
    "70124008": {
        "Centro Poblado": "CEDEÑO"
    },
    "70124009": {
        "Centro Poblado": "MOLINERO"
    },
    "70124010": {
        "Centro Poblado": "NUEVA ESTACIÓN"
    },
    "70124011": {
        "Centro Poblado": "LA MEJÍA"
    },
    "70124012": {
        "Centro Poblado": "LAS PAVITAS"
    },
    "70124013": {
        "Centro Poblado": "NUEVA ESTRELLA"
    },
    "70124014": {
        "Centro Poblado": "NUEVA FE"
    },
    "70124015": {
        "Centro Poblado": "POMPUMA"
    },
    "70124016": {
        "Centro Poblado": "AGUILAR"
    },
    "70124017": {
        "Centro Poblado": "LOS OSSAS"
    },
    "70124018": {
        "Centro Poblado": "PUEBLO BUHO"
    },
    "70124019": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "70124020": {
        "Centro Poblado": "PUNTA ALFEREZ"
    },
    "70124021": {
        "Centro Poblado": "TANGA SOLA"
    },
    "70204000": {
        "Centro Poblado": "RICAURTE (COLOSÓ)"
    },
    "70204002": {
        "Centro Poblado": "CHINULITO"
    },
    "70204005": {
        "Centro Poblado": "BAJO DON JUAN"
    },
    "70204006": {
        "Centro Poblado": "EL OJITO"
    },
    "70204008": {
        "Centro Poblado": "CALLE LARGA"
    },
    "70204009": {
        "Centro Poblado": "CORAZA"
    },
    "70204010": {
        "Centro Poblado": "DESBARRANCADO"
    },
    "70204011": {
        "Centro Poblado": "EL PARAISO"
    },
    "70204012": {
        "Centro Poblado": "LA CEIBA"
    },
    "70204013": {
        "Centro Poblado": "LA ESTACION"
    },
    "70204014": {
        "Centro Poblado": "MARATHON"
    },
    "70204015": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "70215000": {
        "Centro Poblado": "COROZAL"
    },
    "70215001": {
        "Centro Poblado": "CANTAGALLO"
    },
    "70215004": {
        "Centro Poblado": "CHAPINERO"
    },
    "70215005": {
        "Centro Poblado": "DON ALONSO"
    },
    "70215006": {
        "Centro Poblado": "EL MAMÓN"
    },
    "70215009": {
        "Centro Poblado": "HATO NUEVO"
    },
    "70215010": {
        "Centro Poblado": "LAS LLANADAS"
    },
    "70215011": {
        "Centro Poblado": "LAS TINAS"
    },
    "70215014": {
        "Centro Poblado": "SAN JOSE DE PILETA"
    },
    "70215016": {
        "Centro Poblado": "EL RINCON DE LAS FLORES"
    },
    "70215018": {
        "Centro Poblado": "LAS PEÑAS"
    },
    "70215019": {
        "Centro Poblado": "CALLE NUEVA"
    },
    "70215021": {
        "Centro Poblado": "LAS BRUJAS"
    },
    "70215022": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "70215023": {
        "Centro Poblado": "MILAN"
    },
    "70215024": {
        "Centro Poblado": "PALMA SOLA"
    },
    "70215025": {
        "Centro Poblado": "LAS PALMAS"
    },
    "70215026": {
        "Centro Poblado": "HATO VIEJO"
    },
    "70221000": {
        "Centro Poblado": "COVEÑAS"
    },
    "70221001": {
        "Centro Poblado": "BOCA DE LA CIÉNAGA"
    },
    "70221002": {
        "Centro Poblado": "EL REPARO"
    },
    "70221004": {
        "Centro Poblado": "PUNTA SECA"
    },
    "70221005": {
        "Centro Poblado": "EL MAMEY"
    },
    "70221006": {
        "Centro Poblado": "BELLAVISTA"
    },
    "70230000": {
        "Centro Poblado": "CHALÁN"
    },
    "70230001": {
        "Centro Poblado": "LA CEIBA"
    },
    "70230003": {
        "Centro Poblado": "NUEVO MANZANARES"
    },
    "70230004": {
        "Centro Poblado": "DESBARRANCADO"
    },
    "70230006": {
        "Centro Poblado": "MONTEBELLO"
    },
    "70233000": {
        "Centro Poblado": "EL ROBLE"
    },
    "70233001": {
        "Centro Poblado": "CALLEJÓN"
    },
    "70233002": {
        "Centro Poblado": "CAYO DE PALMA"
    },
    "70233003": {
        "Centro Poblado": "CORNETA"
    },
    "70233004": {
        "Centro Poblado": "EL SITIO"
    },
    "70233005": {
        "Centro Poblado": "LAS TABLITAS"
    },
    "70233006": {
        "Centro Poblado": "PALMITAL"
    },
    "70233007": {
        "Centro Poblado": "PATILLAL"
    },
    "70233008": {
        "Centro Poblado": "GRILLO ALEGRE"
    },
    "70233009": {
        "Centro Poblado": "RANCHO DE LA CRUZ"
    },
    "70233010": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "70233011": {
        "Centro Poblado": "SANTA ROSA"
    },
    "70233012": {
        "Centro Poblado": "TIERRA SANTA"
    },
    "70233013": {
        "Centro Poblado": "VILLAVICENCIO"
    },
    "70235000": {
        "Centro Poblado": "GALERAS"
    },
    "70235001": {
        "Centro Poblado": "BARAYA"
    },
    "70235002": {
        "Centro Poblado": "SAN ANDRÉS DE PALOMO"
    },
    "70235003": {
        "Centro Poblado": "SAN JOSÉ DE RIVERA"
    },
    "70235007": {
        "Centro Poblado": "PUEBLO NUEVO II"
    },
    "70235009": {
        "Centro Poblado": "PUEBLO NUEVO I (JUNÍN)"
    },
    "70235011": {
        "Centro Poblado": "PUERTO FRANCO"
    },
    "70235012": {
        "Centro Poblado": "ABRE EL OJO"
    },
    "70235013": {
        "Centro Poblado": "MATA DE GUASIMO"
    },
    "70265000": {
        "Centro Poblado": "GUARANDA"
    },
    "70265002": {
        "Centro Poblado": "DIAZGRANADOS"
    },
    "70265004": {
        "Centro Poblado": "GAVALDA"
    },
    "70265006": {
        "Centro Poblado": "LA CONCORDIA"
    },
    "70265008": {
        "Centro Poblado": "PALMARITICO"
    },
    "70265009": {
        "Centro Poblado": "PUERTO LÓPEZ"
    },
    "70265010": {
        "Centro Poblado": "LA CEJA"
    },
    "70265011": {
        "Centro Poblado": "LAS PAVAS"
    },
    "70265012": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "70265013": {
        "Centro Poblado": "TIERRA SANTA"
    },
    "70400000": {
        "Centro Poblado": "LA UNIÓN"
    },
    "70400001": {
        "Centro Poblado": "CAYO DELGADO"
    },
    "70400002": {
        "Centro Poblado": "PAJARITO"
    },
    "70400004": {
        "Centro Poblado": "LAS PALMITAS"
    },
    "70400005": {
        "Centro Poblado": "SABANETA"
    },
    "70400006": {
        "Centro Poblado": "BOCA NEGRA"
    },
    "70400007": {
        "Centro Poblado": "CONGUITOS"
    },
    "70400008": {
        "Centro Poblado": "LA GLORIA"
    },
    "70400009": {
        "Centro Poblado": "VILLA FÁTIMA"
    },
    "70400010": {
        "Centro Poblado": "LA CONCEPCION"
    },
    "70418000": {
        "Centro Poblado": "LOS PALMITOS"
    },
    "70418001": {
        "Centro Poblado": "EL COLEY"
    },
    "70418002": {
        "Centro Poblado": "EL PIÑAL"
    },
    "70418003": {
        "Centro Poblado": "PALMAS DE VINO"
    },
    "70418004": {
        "Centro Poblado": "SABANAS DE BELTRÁN"
    },
    "70418005": {
        "Centro Poblado": "SABANAS DE PEDRO"
    },
    "70418006": {
        "Centro Poblado": "EL HATILLO"
    },
    "70418010": {
        "Centro Poblado": "CHARCON"
    },
    "70418011": {
        "Centro Poblado": "PALMITO"
    },
    "70418012": {
        "Centro Poblado": "SAN JAIME"
    },
    "70429000": {
        "Centro Poblado": "MAJAGUAL"
    },
    "70429002": {
        "Centro Poblado": "EL NARANJO"
    },
    "70429005": {
        "Centro Poblado": "LA SIERPE"
    },
    "70429006": {
        "Centro Poblado": "LAS PALMITAS"
    },
    "70429008": {
        "Centro Poblado": "PIZA"
    },
    "70429009": {
        "Centro Poblado": "PUEBLONUEVO"
    },
    "70429010": {
        "Centro Poblado": "SAN ROQUE"
    },
    "70429011": {
        "Centro Poblado": "SANTANDER"
    },
    "70429013": {
        "Centro Poblado": "ZAPATA"
    },
    "70429014": {
        "Centro Poblado": "SINCELEJITO"
    },
    "70429016": {
        "Centro Poblado": "LEÓN BLANCO"
    },
    "70429023": {
        "Centro Poblado": "LOS PATOS"
    },
    "70429025": {
        "Centro Poblado": "PALMARITO"
    },
    "70429026": {
        "Centro Poblado": "BOCA DE LAS MUJERES"
    },
    "70429027": {
        "Centro Poblado": "EL INDIO NUEVO"
    },
    "70429028": {
        "Centro Poblado": "EL PALOMAR"
    },
    "70429029": {
        "Centro Poblado": "RIO FRIO"
    },
    "70429031": {
        "Centro Poblado": "CORONCORO"
    },
    "70473000": {
        "Centro Poblado": "MORROA"
    },
    "70473002": {
        "Centro Poblado": "EL RINCÓN"
    },
    "70473003": {
        "Centro Poblado": "EL YESO"
    },
    "70473004": {
        "Centro Poblado": "LAS FLORES"
    },
    "70473005": {
        "Centro Poblado": "SABANETA"
    },
    "70473006": {
        "Centro Poblado": "TUMBATORO"
    },
    "70473009": {
        "Centro Poblado": "SABANAS DE CALI"
    },
    "70473011": {
        "Centro Poblado": "BREMEN"
    },
    "70473012": {
        "Centro Poblado": "EL RECREO"
    },
    "70473013": {
        "Centro Poblado": "EL TOLIMA"
    },
    "70473014": {
        "Centro Poblado": "LA VICTORIA"
    },
    "70473015": {
        "Centro Poblado": "PICHILIN"
    },
    "70508000": {
        "Centro Poblado": "OVEJAS"
    },
    "70508001": {
        "Centro Poblado": "ALMAGRA"
    },
    "70508002": {
        "Centro Poblado": "CANUTAL"
    },
    "70508003": {
        "Centro Poblado": "CANUTALITO"
    },
    "70508004": {
        "Centro Poblado": "CHENGUE"
    },
    "70508005": {
        "Centro Poblado": "DAMASCO"
    },
    "70508006": {
        "Centro Poblado": "DON GABRIEL"
    },
    "70508007": {
        "Centro Poblado": "EL FLORAL"
    },
    "70508009": {
        "Centro Poblado": "FLOR DEL MONTE"
    },
    "70508011": {
        "Centro Poblado": "LA PEÑA"
    },
    "70508012": {
        "Centro Poblado": "OSOS"
    },
    "70508013": {
        "Centro Poblado": "PIJIGUAY"
    },
    "70508014": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "70508015": {
        "Centro Poblado": "SALITRAL"
    },
    "70508018": {
        "Centro Poblado": "SAN RAFAEL ALTO"
    },
    "70508026": {
        "Centro Poblado": "PEDREGAL"
    },
    "70508027": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "70508031": {
        "Centro Poblado": "ZAPATO # 2 PIJIGUAY"
    },
    "70508033": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "70508034": {
        "Centro Poblado": "ALEMANIA"
    },
    "70523000": {
        "Centro Poblado": "PALMITO"
    },
    "70523001": {
        "Centro Poblado": "ALGODONCILLO"
    },
    "70523003": {
        "Centro Poblado": "GUAMI"
    },
    "70523006": {
        "Centro Poblado": "CHUMPUNDÚN"
    },
    "70523007": {
        "Centro Poblado": "EL MARTILLO"
    },
    "70523008": {
        "Centro Poblado": "EL PALMAR BRILLANTE"
    },
    "70523010": {
        "Centro Poblado": "LOS CASTILLOS"
    },
    "70523011": {
        "Centro Poblado": "MEDIA SOMBRA"
    },
    "70523012": {
        "Centro Poblado": "PUEBLECITO"
    },
    "70523013": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "70523014": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "70523017": {
        "Centro Poblado": "LA GRANVIA"
    },
    "70523018": {
        "Centro Poblado": "LOS OLIVOS"
    },
    "70523019": {
        "Centro Poblado": "SAN MARTÍN"
    },
    "70523020": {
        "Centro Poblado": "LAS HUERTAS"
    },
    "70670000": {
        "Centro Poblado": "SAMPUÉS"
    },
    "70670001": {
        "Centro Poblado": "BOSSA NAVARRO"
    },
    "70670002": {
        "Centro Poblado": "CEJA DEL MANGO"
    },
    "70670003": {
        "Centro Poblado": "ESCOBAR ABAJO"
    },
    "70670004": {
        "Centro Poblado": "ESCOBAR ARRIBA"
    },
    "70670007": {
        "Centro Poblado": "MATEO PÉREZ"
    },
    "70670008": {
        "Centro Poblado": "SANTA INÉS DE PALITO"
    },
    "70670009": {
        "Centro Poblado": "PIEDRAS BLANCAS"
    },
    "70670010": {
        "Centro Poblado": "SABANALARGA"
    },
    "70670011": {
        "Centro Poblado": "SAN LUIS"
    },
    "70670012": {
        "Centro Poblado": "SEGOVIA"
    },
    "70670013": {
        "Centro Poblado": "ACHIOTE ARRIBA"
    },
    "70670018": {
        "Centro Poblado": "MATA DE CAÑA"
    },
    "70670023": {
        "Centro Poblado": "ACHIOTE ABAJO"
    },
    "70670024": {
        "Centro Poblado": "SANTA TERESA"
    },
    "70678000": {
        "Centro Poblado": "SAN BENITO ABAD"
    },
    "70678002": {
        "Centro Poblado": "CUIVA"
    },
    "70678003": {
        "Centro Poblado": "JEGUA"
    },
    "70678004": {
        "Centro Poblado": "LA CEIBA"
    },
    "70678007": {
        "Centro Poblado": "PUNTA DE BLANCO"
    },
    "70678009": {
        "Centro Poblado": "SAN ROQUE"
    },
    "70678010": {
        "Centro Poblado": "SANTIAGO APOSTOL"
    },
    "70678011": {
        "Centro Poblado": "DOÑA ANA"
    },
    "70678012": {
        "Centro Poblado": "GUAYABAL"
    },
    "70678013": {
        "Centro Poblado": "EL LIMÓN"
    },
    "70678015": {
        "Centro Poblado": "LA VENTURA"
    },
    "70678019": {
        "Centro Poblado": "HONDURAS"
    },
    "70678020": {
        "Centro Poblado": "PUNTA NUEVA"
    },
    "70678025": {
        "Centro Poblado": "CISPATACA"
    },
    "70678026": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "70678027": {
        "Centro Poblado": "VILLA NUEVA"
    },
    "70678028": {
        "Centro Poblado": "CORRAL VIEJO - LOS ANGELES"
    },
    "70678032": {
        "Centro Poblado": "LA MOLINA"
    },
    "70678033": {
        "Centro Poblado": "LAS CHISPAS"
    },
    "70678034": {
        "Centro Poblado": "RANCHO LA TÍA"
    },
    "70678035": {
        "Centro Poblado": "CALLE NUEVA"
    },
    "70678036": {
        "Centro Poblado": "EMPRESA COLOMBIA"
    },
    "70678037": {
        "Centro Poblado": "LA PLAZA"
    },
    "70678038": {
        "Centro Poblado": "LAS POZAS"
    },
    "70678039": {
        "Centro Poblado": "REMOLINO"
    },
    "70702000": {
        "Centro Poblado": "BETULIA"
    },
    "70702001": {
        "Centro Poblado": "ALBANIA"
    },
    "70702004": {
        "Centro Poblado": "SABANETA"
    },
    "70702005": {
        "Centro Poblado": "VILLA LÓPEZ"
    },
    "70702006": {
        "Centro Poblado": "LAS CRUCES"
    },
    "70702007": {
        "Centro Poblado": "LOMA ALTA"
    },
    "70702008": {
        "Centro Poblado": "SANTO TOMÁS"
    },
    "70702009": {
        "Centro Poblado": "EL SOCORRO"
    },
    "70702010": {
        "Centro Poblado": "GARRAPATERO"
    },
    "70702011": {
        "Centro Poblado": "LOMA DEL LATIGO"
    },
    "70708000": {
        "Centro Poblado": "SAN MARCOS"
    },
    "70708001": {
        "Centro Poblado": "BELÉN"
    },
    "70708002": {
        "Centro Poblado": "BUENAVISTA"
    },
    "70708003": {
        "Centro Poblado": "CANDELARIA"
    },
    "70708004": {
        "Centro Poblado": "CAÑO PRIETO"
    },
    "70708005": {
        "Centro Poblado": "CUENCA"
    },
    "70708006": {
        "Centro Poblado": "EL LIMÓN"
    },
    "70708007": {
        "Centro Poblado": "EL TABLÓN"
    },
    "70708009": {
        "Centro Poblado": "LAS FLORES"
    },
    "70708010": {
        "Centro Poblado": "MONTEGRANDE"
    },
    "70708011": {
        "Centro Poblado": "PALO ALTO"
    },
    "70708012": {
        "Centro Poblado": "EL PITAL"
    },
    "70708013": {
        "Centro Poblado": "SANTA INÉS"
    },
    "70708014": {
        "Centro Poblado": "LA QUEBRADA"
    },
    "70708015": {
        "Centro Poblado": "EL LLANO"
    },
    "70708017": {
        "Centro Poblado": "NEIVA"
    },
    "70708018": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "70708020": {
        "Centro Poblado": "CASTILLERA"
    },
    "70708021": {
        "Centro Poblado": "CAYO DE LA CRUZ"
    },
    "70708024": {
        "Centro Poblado": "EL OASIS"
    },
    "70708025": {
        "Centro Poblado": "LA COSTERA"
    },
    "70708027": {
        "Centro Poblado": "RINCÓN GUERRANO"
    },
    "70708028": {
        "Centro Poblado": "SAN FELIPE"
    },
    "70708029": {
        "Centro Poblado": "SEHEBE"
    },
    "70708030": {
        "Centro Poblado": "CAIMITICO"
    },
    "70708031": {
        "Centro Poblado": "CAÑO CARATE"
    },
    "70708032": {
        "Centro Poblado": "CEJA LARGA"
    },
    "70708033": {
        "Centro Poblado": "EL REPARO"
    },
    "70708034": {
        "Centro Poblado": "MEDIA TAPA"
    },
    "70708035": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "70708036": {
        "Centro Poblado": "PAJONAL"
    },
    "70713000": {
        "Centro Poblado": "SAN ONOFRE"
    },
    "70713001": {
        "Centro Poblado": "AGUACATE"
    },
    "70713002": {
        "Centro Poblado": "BERLÍN"
    },
    "70713003": {
        "Centro Poblado": "BERRUGAS"
    },
    "70713005": {
        "Centro Poblado": "LABARCÉS"
    },
    "70713006": {
        "Centro Poblado": "LIBERTAD"
    },
    "70713007": {
        "Centro Poblado": "PAJONAL"
    },
    "70713008": {
        "Centro Poblado": "PALO ALTO"
    },
    "70713009": {
        "Centro Poblado": "PLANPAREJO"
    },
    "70713010": {
        "Centro Poblado": "RINCÓN DEL MAR"
    },
    "70713011": {
        "Centro Poblado": "SABANAS DE MUCACAL"
    },
    "70713012": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "70713014": {
        "Centro Poblado": "HIGUERÓN"
    },
    "70713015": {
        "Centro Poblado": "EL CHICHO"
    },
    "70713016": {
        "Centro Poblado": "BARRANCAS"
    },
    "70713017": {
        "Centro Poblado": "CERRO DE LAS CASAS"
    },
    "70713018": {
        "Centro Poblado": "PAJONALITO"
    },
    "70713019": {
        "Centro Poblado": "EL PUEBLITO"
    },
    "70713020": {
        "Centro Poblado": "AGUAS NEGRAS"
    },
    "70713021": {
        "Centro Poblado": "PALACIOS"
    },
    "70713022": {
        "Centro Poblado": "BOCACERRADA"
    },
    "70713023": {
        "Centro Poblado": "PALMIRA"
    },
    "70713024": {
        "Centro Poblado": "ALTOS DE JULIO"
    },
    "70713025": {
        "Centro Poblado": "ARROYO SECO"
    },
    "70713026": {
        "Centro Poblado": "LAS BRISAS"
    },
    "70713027": {
        "Centro Poblado": "PISISI"
    },
    "70713028": {
        "Centro Poblado": "SABANAS DE RINCÓN"
    },
    "70713029": {
        "Centro Poblado": "SABANETICA"
    },
    "70713030": {
        "Centro Poblado": "BUENAVENTURA"
    },
    "70713031": {
        "Centro Poblado": "EL CAMPAMENTO"
    },
    "70713032": {
        "Centro Poblado": "EMBOCADA H PAJONAL"
    },
    "70717000": {
        "Centro Poblado": "SAN PEDRO"
    },
    "70717001": {
        "Centro Poblado": "SAN MATEO"
    },
    "70717002": {
        "Centro Poblado": "ROVIRA"
    },
    "70717003": {
        "Centro Poblado": "NUMANCIA"
    },
    "70717004": {
        "Centro Poblado": "EL BAJO DE LA ALEGRÍA"
    },
    "70717006": {
        "Centro Poblado": "CALABOZO"
    },
    "70717007": {
        "Centro Poblado": "EL CARMEN"
    },
    "70717008": {
        "Centro Poblado": "LOS CHIJETES"
    },
    "70717009": {
        "Centro Poblado": "MANIZALES"
    },
    "70717011": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "70742000": {
        "Centro Poblado": "SINCÉ"
    },
    "70742002": {
        "Centro Poblado": "BAZÁN"
    },
    "70742004": {
        "Centro Poblado": "COCOROTE"
    },
    "70742005": {
        "Centro Poblado": "GRANADA"
    },
    "70742008": {
        "Centro Poblado": "LOS LIMONES"
    },
    "70742010": {
        "Centro Poblado": "VALENCIA"
    },
    "70742011": {
        "Centro Poblado": "VÉLEZ"
    },
    "70742013": {
        "Centro Poblado": "LA VIVIENDA"
    },
    "70742014": {
        "Centro Poblado": "PERENDENGUE"
    },
    "70742015": {
        "Centro Poblado": "GALÁPAGO"
    },
    "70742016": {
        "Centro Poblado": "MORALITO"
    },
    "70742017": {
        "Centro Poblado": "PORVENIR"
    },
    "70771000": {
        "Centro Poblado": "SUCRE"
    },
    "70771001": {
        "Centro Poblado": "ARBOLEDA"
    },
    "70771005": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "70771006": {
        "Centro Poblado": "CÓRDOBA"
    },
    "70771008": {
        "Centro Poblado": "EL CONGRESO"
    },
    "70771012": {
        "Centro Poblado": "LA VENTURA"
    },
    "70771013": {
        "Centro Poblado": "MONTERÍA"
    },
    "70771015": {
        "Centro Poblado": "NARANJAL"
    },
    "70771016": {
        "Centro Poblado": "NARIÑO"
    },
    "70771017": {
        "Centro Poblado": "OREJERO"
    },
    "70771018": {
        "Centro Poblado": "SAN LUIS"
    },
    "70771019": {
        "Centro Poblado": "TRAVESÍA"
    },
    "70771020": {
        "Centro Poblado": "HATO NUEVO"
    },
    "70771021": {
        "Centro Poblado": "PAMPANILLA"
    },
    "70771024": {
        "Centro Poblado": "LA PALMA"
    },
    "70771027": {
        "Centro Poblado": "SAN MATEO"
    },
    "70771053": {
        "Centro Poblado": "TOTUMAL"
    },
    "70820000": {
        "Centro Poblado": "SANTIAGO DE TOLÚ"
    },
    "70820003": {
        "Centro Poblado": "NUEVA ERA"
    },
    "70820007": {
        "Centro Poblado": "PITA EN MEDIO"
    },
    "70820008": {
        "Centro Poblado": "PUERTO VIEJO"
    },
    "70820010": {
        "Centro Poblado": "PITA ABAJO"
    },
    "70820013": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "70823000": {
        "Centro Poblado": "TOLUVIEJO"
    },
    "70823001": {
        "Centro Poblado": "CARACOL"
    },
    "70823002": {
        "Centro Poblado": "LAS PIEDRAS"
    },
    "70823003": {
        "Centro Poblado": "MACAJÁN"
    },
    "70823004": {
        "Centro Poblado": "PALMIRA"
    },
    "70823005": {
        "Centro Poblado": "VARSOVIA"
    },
    "70823006": {
        "Centro Poblado": "LA PICHE"
    },
    "70823007": {
        "Centro Poblado": "CIENAGUITA"
    },
    "70823009": {
        "Centro Poblado": "MOQUEN"
    },
    "70823010": {
        "Centro Poblado": "GUALÓN"
    },
    "70823011": {
        "Centro Poblado": "CAÑITO"
    },
    "70823012": {
        "Centro Poblado": "LA SIRIA"
    },
    "70823013": {
        "Centro Poblado": "LA FLORESTA"
    },
    "70823014": {
        "Centro Poblado": "LOS ALTOS"
    },
    "70823015": {
        "Centro Poblado": "NUEVA ESPERANZA"
    },
    "73001000": {
        "Centro Poblado": "IBAGUÉ"
    },
    "73001001": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "73001004": {
        "Centro Poblado": "DANTAS"
    },
    "73001006": {
        "Centro Poblado": "JUNTAS"
    },
    "73001007": {
        "Centro Poblado": "LAURELES"
    },
    "73001009": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "73001010": {
        "Centro Poblado": "SAN JUAN DE LA CHINA"
    },
    "73001011": {
        "Centro Poblado": "TAPIAS"
    },
    "73001012": {
        "Centro Poblado": "TOCHE"
    },
    "73001013": {
        "Centro Poblado": "VILLARESTREPO"
    },
    "73001014": {
        "Centro Poblado": "LLANITOS"
    },
    "73001015": {
        "Centro Poblado": "EL TOTUMO"
    },
    "73001016": {
        "Centro Poblado": "LLANO DEL COMBEIMA"
    },
    "73001017": {
        "Centro Poblado": "CARMEN DE BULIRA"
    },
    "73001018": {
        "Centro Poblado": "EL RODEO"
    },
    "73001020": {
        "Centro Poblado": "COELLO - COCORA"
    },
    "73001024": {
        "Centro Poblado": "SANTA TERESA"
    },
    "73001025": {
        "Centro Poblado": "PASTALES VIEJO"
    },
    "73001027": {
        "Centro Poblado": "PASTALES NUEVO"
    },
    "73001028": {
        "Centro Poblado": "LA FLOR"
    },
    "73001030": {
        "Centro Poblado": "EL CAY"
    },
    "73001032": {
        "Centro Poblado": "ALTO DE GUALANDAY"
    },
    "73001034": {
        "Centro Poblado": "APARCO"
    },
    "73001036": {
        "Centro Poblado": "BRICEÑO"
    },
    "73001038": {
        "Centro Poblado": "CHEMBE"
    },
    "73001039": {
        "Centro Poblado": "CHUCUNÍ"
    },
    "73001047": {
        "Centro Poblado": "LA HELENA"
    },
    "73001049": {
        "Centro Poblado": "LA MIEL"
    },
    "73001050": {
        "Centro Poblado": "LA PALMILLA"
    },
    "73001057": {
        "Centro Poblado": "LOS TÚNELES"
    },
    "73001058": {
        "Centro Poblado": "PICO DE ORO"
    },
    "73001059": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "73001065": {
        "Centro Poblado": "INVASION BELLA ISLA DE LLANITOS"
    },
    "73001066": {
        "Centro Poblado": "SALITRE"
    },
    "73024000": {
        "Centro Poblado": "ALPUJARRA"
    },
    "73024001": {
        "Centro Poblado": "LA ARADA"
    },
    "73024002": {
        "Centro Poblado": "EL CARMEN"
    },
    "73024003": {
        "Centro Poblado": "AMESES"
    },
    "73026000": {
        "Centro Poblado": "ALVARADO"
    },
    "73026001": {
        "Centro Poblado": "CALDAS VIEJO"
    },
    "73026004": {
        "Centro Poblado": "RINCÓN CHIPALO"
    },
    "73026005": {
        "Centro Poblado": "VERACRUZ"
    },
    "73026008": {
        "Centro Poblado": "LA TEBAIDA"
    },
    "73026011": {
        "Centro Poblado": "TOTARITO"
    },
    "73030000": {
        "Centro Poblado": "AMBALEMA"
    },
    "73030002": {
        "Centro Poblado": "CHORRILLO"
    },
    "73030004": {
        "Centro Poblado": "PAJONALES"
    },
    "73030006": {
        "Centro Poblado": "LA ALDEA EL DANUBIO"
    },
    "73030007": {
        "Centro Poblado": "BOQUERÓN"
    },
    "73043000": {
        "Centro Poblado": "ANZOÁTEGUI"
    },
    "73043001": {
        "Centro Poblado": "LISBOA"
    },
    "73043002": {
        "Centro Poblado": "PALOMAR"
    },
    "73043003": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "73055000": {
        "Centro Poblado": "GUAYABAL"
    },
    "73055002": {
        "Centro Poblado": "MÉNDEZ"
    },
    "73055003": {
        "Centro Poblado": "SAN PEDRO"
    },
    "73055004": {
        "Centro Poblado": "SAN FELIPE"
    },
    "73055006": {
        "Centro Poblado": "FUNDADORES"
    },
    "73055007": {
        "Centro Poblado": "NUEVO HORIZONTE"
    },
    "73067000": {
        "Centro Poblado": "ATACO"
    },
    "73067001": {
        "Centro Poblado": "CAMPOHERMOSO"
    },
    "73067003": {
        "Centro Poblado": "CASA DE ZINC"
    },
    "73067005": {
        "Centro Poblado": "MESA DE POLE"
    },
    "73067006": {
        "Centro Poblado": "POLECITO"
    },
    "73067007": {
        "Centro Poblado": "SANTIAGO PÉREZ"
    },
    "73067012": {
        "Centro Poblado": "MONTELORO"
    },
    "73067014": {
        "Centro Poblado": "EL PAUJIL"
    },
    "73067016": {
        "Centro Poblado": "CÓNDOR"
    },
    "73067020": {
        "Centro Poblado": "EL BALSO"
    },
    "73067021": {
        "Centro Poblado": "LA LAGUNA"
    },
    "73067022": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "73124000": {
        "Centro Poblado": "CAJAMARCA"
    },
    "73124001": {
        "Centro Poblado": "ANAIME"
    },
    "73124005": {
        "Centro Poblado": "EL ROSAL"
    },
    "73148000": {
        "Centro Poblado": "CARMEN DE APICALÁ"
    },
    "73152000": {
        "Centro Poblado": "CASABIANCA"
    },
    "73152002": {
        "Centro Poblado": "SAN JERÓNIMO"
    },
    "73168000": {
        "Centro Poblado": "CHAPARRAL"
    },
    "73168004": {
        "Centro Poblado": "EL LIMÓN"
    },
    "73168005": {
        "Centro Poblado": "LA MARINA"
    },
    "73168006": {
        "Centro Poblado": "LA PROFUNDA"
    },
    "73168007": {
        "Centro Poblado": "SAN JOSÉ DE LAS HERMOSAS"
    },
    "73200000": {
        "Centro Poblado": "COELLO"
    },
    "73200001": {
        "Centro Poblado": "GUALANDAY"
    },
    "73200002": {
        "Centro Poblado": "LA BARRIALOSA"
    },
    "73200003": {
        "Centro Poblado": "LLANO DE LA VIRGEN"
    },
    "73200004": {
        "Centro Poblado": "POTRERILLO"
    },
    "73200005": {
        "Centro Poblado": "VEGA LOS PADRES"
    },
    "73200016": {
        "Centro Poblado": "VINDI"
    },
    "73200017": {
        "Centro Poblado": "CALABOZO"
    },
    "73217000": {
        "Centro Poblado": "COYAIMA"
    },
    "73217001": {
        "Centro Poblado": "CASTILLA"
    },
    "73217005": {
        "Centro Poblado": "TOTARCO DINDE"
    },
    "73217011": {
        "Centro Poblado": "GUAYAQUIL"
    },
    "73217012": {
        "Centro Poblado": "MESA DE INCA"
    },
    "73217013": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "73226000": {
        "Centro Poblado": "CUNDAY"
    },
    "73226001": {
        "Centro Poblado": "LA AURORA"
    },
    "73226002": {
        "Centro Poblado": "SAN PABLO"
    },
    "73226003": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "73226004": {
        "Centro Poblado": "VALENCIA"
    },
    "73226005": {
        "Centro Poblado": "VARSOVIA"
    },
    "73226008": {
        "Centro Poblado": "EL REVÉS"
    },
    "73236000": {
        "Centro Poblado": "DOLORES"
    },
    "73236004": {
        "Centro Poblado": "RIONEGRO"
    },
    "73236005": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "73236007": {
        "Centro Poblado": "LOS LLANITOS"
    },
    "73236010": {
        "Centro Poblado": "LA SOLEDAD"
    },
    "73236011": {
        "Centro Poblado": "SAN PEDRO"
    },
    "73268000": {
        "Centro Poblado": "EL ESPINAL"
    },
    "73268001": {
        "Centro Poblado": "CHICORAL"
    },
    "73268003": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "73270000": {
        "Centro Poblado": "FALAN"
    },
    "73270001": {
        "Centro Poblado": "FRÍAS"
    },
    "73270004": {
        "Centro Poblado": "PIEDECUESTA"
    },
    "73275000": {
        "Centro Poblado": "FLANDES"
    },
    "73275001": {
        "Centro Poblado": "EL COLEGIO"
    },
    "73275005": {
        "Centro Poblado": "PARADERO I"
    },
    "73275009": {
        "Centro Poblado": "CONDOMINIO SANTA ANA Y PALMA REAL"
    },
    "73275010": {
        "Centro Poblado": "CONDOMINIO VILLA ESPERANZA"
    },
    "73283000": {
        "Centro Poblado": "FRESNO"
    },
    "73283001": {
        "Centro Poblado": "BETANIA"
    },
    "73283003": {
        "Centro Poblado": "EL TABLAZO"
    },
    "73283004": {
        "Centro Poblado": "LA AGUADITA"
    },
    "73283008": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "73283013": {
        "Centro Poblado": "PARTIDAS"
    },
    "73319000": {
        "Centro Poblado": "GUAMO"
    },
    "73319002": {
        "Centro Poblado": "LA CHAMBA"
    },
    "73319004": {
        "Centro Poblado": "RINCÓN SANTO CENTRO"
    },
    "73319005": {
        "Centro Poblado": "CHIPUELO ORIENTE"
    },
    "73319009": {
        "Centro Poblado": "LA TROJA"
    },
    "73319010": {
        "Centro Poblado": "LOMA DE LUISA"
    },
    "73319013": {
        "Centro Poblado": "CAÑADA EL RODEO"
    },
    "73319015": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "73319016": {
        "Centro Poblado": "CEREZUELA LAS GARZAS"
    },
    "73347000": {
        "Centro Poblado": "HERVEO"
    },
    "73347001": {
        "Centro Poblado": "BRASIL"
    },
    "73347003": {
        "Centro Poblado": "LETRAS"
    },
    "73347004": {
        "Centro Poblado": "MESONES"
    },
    "73347005": {
        "Centro Poblado": "PADUA"
    },
    "73349000": {
        "Centro Poblado": "HONDA"
    },
    "73349001": {
        "Centro Poblado": "PERICO"
    },
    "73352000": {
        "Centro Poblado": "ICONONZO"
    },
    "73352001": {
        "Centro Poblado": "BALCONCITOS"
    },
    "73352002": {
        "Centro Poblado": "BOQUERÓN"
    },
    "73352003": {
        "Centro Poblado": "MUNDO NUEVO"
    },
    "73352005": {
        "Centro Poblado": "PATECUINDE"
    },
    "73352007": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "73408000": {
        "Centro Poblado": "LÉRIDA"
    },
    "73408001": {
        "Centro Poblado": "DELICIAS"
    },
    "73408002": {
        "Centro Poblado": "SAN FRANCISCO DE LA SIERRA"
    },
    "73408003": {
        "Centro Poblado": "PADILLA"
    },
    "73408005": {
        "Centro Poblado": "IGUASITOS"
    },
    "73411000": {
        "Centro Poblado": "LÍBANO"
    },
    "73411002": {
        "Centro Poblado": "CONVENIO"
    },
    "73411006": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "73411007": {
        "Centro Poblado": "SANTA TERESA"
    },
    "73411008": {
        "Centro Poblado": "TIERRADENTRO"
    },
    "73411009": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "73443000": {
        "Centro Poblado": "SAN SEBASTIÁN DE MARIQUITA"
    },
    "73443001": {
        "Centro Poblado": "EL HATILLO"
    },
    "73443002": {
        "Centro Poblado": "LA CABAÑA"
    },
    "73443003": {
        "Centro Poblado": "PITALITO"
    },
    "73443004": {
        "Centro Poblado": "LA ALBANIA"
    },
    "73443006": {
        "Centro Poblado": "CAMELIAS"
    },
    "73443008": {
        "Centro Poblado": "LA PARROQUIA"
    },
    "73443009": {
        "Centro Poblado": "LAS MARÍAS"
    },
    "73449000": {
        "Centro Poblado": "MELGAR"
    },
    "73449001": {
        "Centro Poblado": "CUALAMANÁ"
    },
    "73449004": {
        "Centro Poblado": "ÁGUILA"
    },
    "73449006": {
        "Centro Poblado": "BALCONES DEL SUMAPAZ"
    },
    "73449008": {
        "Centro Poblado": "EL RUBY"
    },
    "73449009": {
        "Centro Poblado": "LA ESTANCIA"
    },
    "73449012": {
        "Centro Poblado": "QUEBRADITAS 1"
    },
    "73449014": {
        "Centro Poblado": "SAN JOSÉ DE LA COLORADA"
    },
    "73449016": {
        "Centro Poblado": "CUALAMANÁ 2"
    },
    "73449017": {
        "Centro Poblado": "EL PALMAR"
    },
    "73449018": {
        "Centro Poblado": "PEDRO GOMEZ"
    },
    "73461000": {
        "Centro Poblado": "MURILLO"
    },
    "73461001": {
        "Centro Poblado": "EL BOSQUE"
    },
    "73483000": {
        "Centro Poblado": "NATAGAIMA"
    },
    "73483001": {
        "Centro Poblado": "LA PALMITA"
    },
    "73483002": {
        "Centro Poblado": "VELÚ"
    },
    "73483008": {
        "Centro Poblado": "RINCÓN ANCHIQUE"
    },
    "73483012": {
        "Centro Poblado": "LAS BRISAS"
    },
    "73504000": {
        "Centro Poblado": "ORTEGA"
    },
    "73504003": {
        "Centro Poblado": "GUAIPA"
    },
    "73504004": {
        "Centro Poblado": "HATO DE IGLESIA"
    },
    "73504007": {
        "Centro Poblado": "LA MESA DE ORTEGA"
    },
    "73504008": {
        "Centro Poblado": "OLAYA HERRERA"
    },
    "73504009": {
        "Centro Poblado": "EL VERGEL"
    },
    "73504017": {
        "Centro Poblado": "LOS GUAYABOS"
    },
    "73520000": {
        "Centro Poblado": "PALOCABILDO"
    },
    "73520001": {
        "Centro Poblado": "ASTURIAS"
    },
    "73520002": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "73520003": {
        "Centro Poblado": "GUADUALITO"
    },
    "73547000": {
        "Centro Poblado": "PIEDRAS"
    },
    "73547001": {
        "Centro Poblado": "CHICALÁ"
    },
    "73547002": {
        "Centro Poblado": "DOIMA"
    },
    "73547003": {
        "Centro Poblado": "GUATAQUISITO"
    },
    "73547005": {
        "Centro Poblado": "PARADERO CHIPALO"
    },
    "73555000": {
        "Centro Poblado": "PLANADAS"
    },
    "73555001": {
        "Centro Poblado": "BILBAO"
    },
    "73555002": {
        "Centro Poblado": "GAITANIA"
    },
    "73555004": {
        "Centro Poblado": "SUR DE ATA"
    },
    "73555006": {
        "Centro Poblado": "BRUSELAS"
    },
    "73555007": {
        "Centro Poblado": "SAN MIGUEL"
    },
    "73563000": {
        "Centro Poblado": "PRADO"
    },
    "73563001": {
        "Centro Poblado": "ACO"
    },
    "73563004": {
        "Centro Poblado": "MONTOSO"
    },
    "73585000": {
        "Centro Poblado": "PURIFICACIÓN"
    },
    "73585001": {
        "Centro Poblado": "CHENCHE ASOLEADO"
    },
    "73585002": {
        "Centro Poblado": "LOZANIA"
    },
    "73585006": {
        "Centro Poblado": "VILLA ESPERANZA"
    },
    "73585007": {
        "Centro Poblado": "VILLA COLOMBIA"
    },
    "73585009": {
        "Centro Poblado": "EL BAURA"
    },
    "73585013": {
        "Centro Poblado": "LA MATA"
    },
    "73585015": {
        "Centro Poblado": "BUENAVISTA"
    },
    "73585018": {
        "Centro Poblado": "CHENCHE UNO"
    },
    "73616000": {
        "Centro Poblado": "RIOBLANCO"
    },
    "73616001": {
        "Centro Poblado": "HERRERA"
    },
    "73616002": {
        "Centro Poblado": "PUERTO SALDAÑA"
    },
    "73616004": {
        "Centro Poblado": "PALONEGRO"
    },
    "73616005": {
        "Centro Poblado": "GAITÁN"
    },
    "73616006": {
        "Centro Poblado": "MARACAIBO"
    },
    "73616009": {
        "Centro Poblado": "JUNTAS"
    },
    "73622000": {
        "Centro Poblado": "RONCESVALLES"
    },
    "73622001": {
        "Centro Poblado": "SANTA ELENA"
    },
    "73622002": {
        "Centro Poblado": "EL CEDRO"
    },
    "73624000": {
        "Centro Poblado": "ROVIRA"
    },
    "73624001": {
        "Centro Poblado": "EL CORAZÓN"
    },
    "73624003": {
        "Centro Poblado": "LOS ANDES - LA BELLA"
    },
    "73624004": {
        "Centro Poblado": "RIOMANSO"
    },
    "73624005": {
        "Centro Poblado": "SAN PEDRO"
    },
    "73624007": {
        "Centro Poblado": "GUADUALITO"
    },
    "73624008": {
        "Centro Poblado": "LA FLORIDA"
    },
    "73624010": {
        "Centro Poblado": "LA SELVA"
    },
    "73624012": {
        "Centro Poblado": "LA LUISA"
    },
    "73671000": {
        "Centro Poblado": "SALDAÑA"
    },
    "73671001": {
        "Centro Poblado": "JABALCÓN"
    },
    "73671002": {
        "Centro Poblado": "SANTA INÉS"
    },
    "73671008": {
        "Centro Poblado": "LA ESPERANZA"
    },
    "73671009": {
        "Centro Poblado": "NORMANDÍA"
    },
    "73675000": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "73675001": {
        "Centro Poblado": "LA FLORIDA"
    },
    "73675002": {
        "Centro Poblado": "PLAYARRICA"
    },
    "73675004": {
        "Centro Poblado": "VILLA HERMOSA"
    },
    "73678000": {
        "Centro Poblado": "SAN LUIS"
    },
    "73678004": {
        "Centro Poblado": "PAYANDÉ"
    },
    "73686000": {
        "Centro Poblado": "SANTA ISABEL"
    },
    "73686001": {
        "Centro Poblado": "COLÓN"
    },
    "73686003": {
        "Centro Poblado": "SAN RAFAEL"
    },
    "73770000": {
        "Centro Poblado": "SUÁREZ"
    },
    "73770001": {
        "Centro Poblado": "HATO VIEJO"
    },
    "73770003": {
        "Centro Poblado": "CAÑAVERALES"
    },
    "73770005": {
        "Centro Poblado": "AGUA BLANCA"
    },
    "73854000": {
        "Centro Poblado": "VALLE DE SAN JUAN"
    },
    "73861000": {
        "Centro Poblado": "VENADILLO"
    },
    "73861001": {
        "Centro Poblado": "JUNÍN"
    },
    "73861002": {
        "Centro Poblado": "LA SIERRITA"
    },
    "73861003": {
        "Centro Poblado": "MALABAR"
    },
    "73861004": {
        "Centro Poblado": "PALMAROSA"
    },
    "73870000": {
        "Centro Poblado": "VILLAHERMOSA"
    },
    "73873000": {
        "Centro Poblado": "VILLARRICA"
    },
    "73873002": {
        "Centro Poblado": "LA COLONIA"
    },
    "73873003": {
        "Centro Poblado": "LOS ALPES"
    },
    "73873004": {
        "Centro Poblado": "PUERTO LLERAS"
    },
    "76001000": {
        "Centro Poblado": "SANTIAGO DE CALI, DISTRITO ESPECIAL, DEPORTIVO, CULTURAL, TURÍSTICO, EMPRESARIAL Y DE SERVICIOS"
    },
    "76001001": {
        "Centro Poblado": "EL SALADITO"
    },
    "76001002": {
        "Centro Poblado": "FELIDIA"
    },
    "76001003": {
        "Centro Poblado": "GOLONDRINAS"
    },
    "76001004": {
        "Centro Poblado": "EL HORMIGUERO"
    },
    "76001005": {
        "Centro Poblado": "LA BUITRERA"
    },
    "76001006": {
        "Centro Poblado": "LA CASTILLA"
    },
    "76001007": {
        "Centro Poblado": "LA ELVIRA"
    },
    "76001008": {
        "Centro Poblado": "LA LEONERA"
    },
    "76001009": {
        "Centro Poblado": "LA PAZ"
    },
    "76001010": {
        "Centro Poblado": "LOS ANDES"
    },
    "76001012": {
        "Centro Poblado": "NAVARRO"
    },
    "76001013": {
        "Centro Poblado": "PANCE"
    },
    "76001014": {
        "Centro Poblado": "PICHINDE"
    },
    "76001016": {
        "Centro Poblado": "MONTEBELLO"
    },
    "76001019": {
        "Centro Poblado": "CASCAJAL II"
    },
    "76001020": {
        "Centro Poblado": "VILLACARMELO"
    },
    "76001022": {
        "Centro Poblado": "BRISAS DE MONTEBELLO"
    },
    "76001023": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "76001024": {
        "Centro Poblado": "CASCAJAL I"
    },
    "76001025": {
        "Centro Poblado": "CRUCERO ALTO DE LOS MANGOS"
    },
    "76001026": {
        "Centro Poblado": "EL FILO"
    },
    "76001027": {
        "Centro Poblado": "EL PORTENTO"
    },
    "76001028": {
        "Centro Poblado": "LA FRAGUA"
    },
    "76001029": {
        "Centro Poblado": "LA VORÁGINE"
    },
    "76001030": {
        "Centro Poblado": "LAS PALMAS"
    },
    "76001031": {
        "Centro Poblado": "LOS CERROS"
    },
    "76001032": {
        "Centro Poblado": "MONTAÑITAS"
    },
    "76001034": {
        "Centro Poblado": "PIZAMOS"
    },
    "76001035": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "76001036": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "76001037": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "76001038": {
        "Centro Poblado": "VILLA FLAMENCO"
    },
    "76001041": {
        "Centro Poblado": "CASCAJAL III"
    },
    "76001042": {
        "Centro Poblado": "EL ESTERO"
    },
    "76001043": {
        "Centro Poblado": "LA LUISA"
    },
    "76001044": {
        "Centro Poblado": "LA SIRENA"
    },
    "76001045": {
        "Centro Poblado": "LAS PALMAS - LA CASTILLA"
    },
    "76001046": {
        "Centro Poblado": "SILOE"
    },
    "76001048": {
        "Centro Poblado": "LOS LIMONES"
    },
    "76001050": {
        "Centro Poblado": "CAUCA VIEJO"
    },
    "76001051": {
        "Centro Poblado": "CONDOMINIO MARAÑON"
    },
    "76001052": {
        "Centro Poblado": "CHORRO DE PLATA"
    },
    "76001053": {
        "Centro Poblado": "PARCELACION CANTACLARO 1"
    },
    "76001054": {
        "Centro Poblado": "PARCELACION CANTACLARO 2"
    },
    "76001055": {
        "Centro Poblado": "PARCELACION LA TRINIDAD"
    },
    "76001056": {
        "Centro Poblado": "PIAMONTE"
    },
    "76001057": {
        "Centro Poblado": "CALLEJON TABARES"
    },
    "76001058": {
        "Centro Poblado": "DUQUELANDIA"
    },
    "76001059": {
        "Centro Poblado": "LA COLINA"
    },
    "76001060": {
        "Centro Poblado": "LOS GIRASOLES"
    },
    "76001061": {
        "Centro Poblado": "PILAS DEL CABUYAL"
    },
    "76001062": {
        "Centro Poblado": "VILLA DEL ROSARIO"
    },
    "76020000": {
        "Centro Poblado": "ALCALÁ"
    },
    "76020006": {
        "Centro Poblado": "LA FLORESTA"
    },
    "76020007": {
        "Centro Poblado": "LA POLONIA"
    },
    "76036000": {
        "Centro Poblado": "ANDALUCÍA"
    },
    "76036002": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "76036003": {
        "Centro Poblado": "EL SALTO"
    },
    "76036006": {
        "Centro Poblado": "TAMBORAL"
    },
    "76036007": {
        "Centro Poblado": "ZANJÓN DE PIEDRA"
    },
    "76036009": {
        "Centro Poblado": "MONTE HERMOSO"
    },
    "76036010": {
        "Centro Poblado": "MADRE VIEJA"
    },
    "76036011": {
        "Centro Poblado": "LA PAZ"
    },
    "76041000": {
        "Centro Poblado": "ANSERMANUEVO"
    },
    "76041001": {
        "Centro Poblado": "ANACARO"
    },
    "76041003": {
        "Centro Poblado": "EL BILLAR"
    },
    "76041006": {
        "Centro Poblado": "EL VERGEL"
    },
    "76041013": {
        "Centro Poblado": "GRAMALOTE"
    },
    "76041021": {
        "Centro Poblado": "SALAZAR"
    },
    "76054000": {
        "Centro Poblado": "ARGELIA"
    },
    "76054004": {
        "Centro Poblado": "EL RAIZAL"
    },
    "76054005": {
        "Centro Poblado": "LA AURORA"
    },
    "76100000": {
        "Centro Poblado": "BOLÍVAR"
    },
    "76100001": {
        "Centro Poblado": "BETANIA"
    },
    "76100002": {
        "Centro Poblado": "CERRO AZUL"
    },
    "76100006": {
        "Centro Poblado": "LA HERRADURA"
    },
    "76100007": {
        "Centro Poblado": "LA TULIA"
    },
    "76100008": {
        "Centro Poblado": "NARANJAL"
    },
    "76100009": {
        "Centro Poblado": "PRIMAVERA"
    },
    "76100010": {
        "Centro Poblado": "RICAURTE"
    },
    "76100012": {
        "Centro Poblado": "AGUAS LINDAS"
    },
    "76100014": {
        "Centro Poblado": "SAN FERNANDO"
    },
    "76109000": {
        "Centro Poblado": "BUENAVENTURA, DISTRITO ESPECIAL, INDUSTRIAL, PORTUARIO, BIODIVERSO Y ECOTURÍSTICO"
    },
    "76109001": {
        "Centro Poblado": "AGUACLARA"
    },
    "76109002": {
        "Centro Poblado": "BARCO"
    },
    "76109003": {
        "Centro Poblado": "LA BOCANA"
    },
    "76109006": {
        "Centro Poblado": "BAJO CALIMA"
    },
    "76109009": {
        "Centro Poblado": "CÓRDOBA"
    },
    "76109012": {
        "Centro Poblado": "PITAL"
    },
    "76109017": {
        "Centro Poblado": "TRIANA"
    },
    "76109018": {
        "Centro Poblado": "CONCEPCIÓN"
    },
    "76109019": {
        "Centro Poblado": "LA PLATA"
    },
    "76109021": {
        "Centro Poblado": "LADRILLEROS"
    },
    "76109022": {
        "Centro Poblado": "LLANO BAJO"
    },
    "76109024": {
        "Centro Poblado": "BOCAS DE MAYORQUIN"
    },
    "76109028": {
        "Centro Poblado": "PUERTO MERIZALDE"
    },
    "76109030": {
        "Centro Poblado": "PUNTA SOLDADO"
    },
    "76109031": {
        "Centro Poblado": "SAN ANTONIO (YURUMANGUÍ)"
    },
    "76109032": {
        "Centro Poblado": "SAN FRANCISCO DE NAYA"
    },
    "76109033": {
        "Centro Poblado": "SAN FRANCISCO JAVIER"
    },
    "76109034": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "76109036": {
        "Centro Poblado": "SAN LORENZO"
    },
    "76109037": {
        "Centro Poblado": "SAN PEDRO"
    },
    "76109038": {
        "Centro Poblado": "SILVA"
    },
    "76109039": {
        "Centro Poblado": "TAPARAL"
    },
    "76109040": {
        "Centro Poblado": "VENERAL"
    },
    "76109041": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "76109042": {
        "Centro Poblado": "SABALETAS"
    },
    "76109043": {
        "Centro Poblado": "ZACARÍAS"
    },
    "76109044": {
        "Centro Poblado": "CABECERA RÍO SAN JUAN"
    },
    "76109045": {
        "Centro Poblado": "LA BARRA"
    },
    "76109046": {
        "Centro Poblado": "JUANCHACO"
    },
    "76109047": {
        "Centro Poblado": "PIANGUITA"
    },
    "76109053": {
        "Centro Poblado": "CHAMUSCADO"
    },
    "76109058": {
        "Centro Poblado": "EL BARRANCO"
    },
    "76109061": {
        "Centro Poblado": "GUAIMIA"
    },
    "76109062": {
        "Centro Poblado": "JUNTAS"
    },
    "76109064": {
        "Centro Poblado": "BARTOLA"
    },
    "76109065": {
        "Centro Poblado": "LA BREA"
    },
    "76109069": {
        "Centro Poblado": "PAPAYAL"
    },
    "76109071": {
        "Centro Poblado": "SAN CIPRIANO"
    },
    "76109074": {
        "Centro Poblado": "SAN JOSÉ DE NAYA"
    },
    "76109076": {
        "Centro Poblado": "SAN MARCOS"
    },
    "76109077": {
        "Centro Poblado": "SANTA CRUZ"
    },
    "76109078": {
        "Centro Poblado": "ZARAGOZA"
    },
    "76109079": {
        "Centro Poblado": "AGUAMANSA"
    },
    "76109080": {
        "Centro Poblado": "CASCAJITA"
    },
    "76109081": {
        "Centro Poblado": "PUNTA BONITA"
    },
    "76109082": {
        "Centro Poblado": "HORIZONTE"
    },
    "76109083": {
        "Centro Poblado": "BENDICIONES"
    },
    "76109084": {
        "Centro Poblado": "EL CACAO"
    },
    "76109085": {
        "Centro Poblado": "CALLE LARGA - AEROPUERTO"
    },
    "76109086": {
        "Centro Poblado": "CAMINO VIEJO - KM 40"
    },
    "76109087": {
        "Centro Poblado": "CAMPO HERMOSO"
    },
    "76109088": {
        "Centro Poblado": "EL CRUCERO"
    },
    "76109089": {
        "Centro Poblado": "EL ENCANTO"
    },
    "76109090": {
        "Centro Poblado": "EL LLANO"
    },
    "76109091": {
        "Centro Poblado": "EL SALTO"
    },
    "76109092": {
        "Centro Poblado": "GUADUALITO"
    },
    "76109093": {
        "Centro Poblado": "JOAQUINCITO RESGUARDO INDIGENA"
    },
    "76109095": {
        "Centro Poblado": "LA BALASTRERA"
    },
    "76109096": {
        "Centro Poblado": "LA COMBA"
    },
    "76109097": {
        "Centro Poblado": "LA CONTRA"
    },
    "76109098": {
        "Centro Poblado": "LA FRAGUA"
    },
    "76109099": {
        "Centro Poblado": "PRIMAVERA"
    },
    "76109100": {
        "Centro Poblado": "LA VUELTA"
    },
    "76109102": {
        "Centro Poblado": "LIMONES"
    },
    "76109104": {
        "Centro Poblado": "PAPAYAL 2"
    },
    "76109106": {
        "Centro Poblado": "SAGRADA FAMILIA"
    },
    "76109107": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76109108": {
        "Centro Poblado": "SAN ANTOÑITO (YURUMANGUI)"
    },
    "76109109": {
        "Centro Poblado": "SAN ISIDRO (CAJAMBRE)"
    },
    "76109110": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "76109111": {
        "Centro Poblado": "SECADERO"
    },
    "76109112": {
        "Centro Poblado": "UMANE"
    },
    "76109113": {
        "Centro Poblado": "VILLA ESTELA"
    },
    "76109115": {
        "Centro Poblado": "ALTO ZARAGOZA"
    },
    "76109116": {
        "Centro Poblado": "BARRIO BUENOS AIRES"
    },
    "76109118": {
        "Centro Poblado": "BRISAS"
    },
    "76109121": {
        "Centro Poblado": "EL PALITO"
    },
    "76109122": {
        "Centro Poblado": "JUAQUINCITO"
    },
    "76109123": {
        "Centro Poblado": "LA BOCANA (VISTA HERMOSA)"
    },
    "76109124": {
        "Centro Poblado": "LA CAUCANA"
    },
    "76109125": {
        "Centro Poblado": "LA LAGUNA"
    },
    "76109127": {
        "Centro Poblado": "SAN ANTONIO 1"
    },
    "76109128": {
        "Centro Poblado": "SAN ANTONIO 2"
    },
    "76109129": {
        "Centro Poblado": "ZARAGOZA ALTO 1"
    },
    "76109130": {
        "Centro Poblado": "ZARAGOZA PUENTE SAN MARTIN 1"
    },
    "76109131": {
        "Centro Poblado": "ZARAGOZA PUENTE SAN MARTIN 2"
    },
    "76111000": {
        "Centro Poblado": "GUADALAJARA DE BUGA"
    },
    "76111001": {
        "Centro Poblado": "LA CAMPIÑA"
    },
    "76111002": {
        "Centro Poblado": "EL PLACER"
    },
    "76111005": {
        "Centro Poblado": "EL VINCULO"
    },
    "76111006": {
        "Centro Poblado": "LA HABANA"
    },
    "76111007": {
        "Centro Poblado": "LA MARÍA"
    },
    "76111012": {
        "Centro Poblado": "QUEBRADASECA"
    },
    "76111014": {
        "Centro Poblado": "ZANJÓN HONDO"
    },
    "76111016": {
        "Centro Poblado": "EL PORVENIR"
    },
    "76111018": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "76111020": {
        "Centro Poblado": "LA MAGDALENA"
    },
    "76111021": {
        "Centro Poblado": "EL MANANTIAL"
    },
    "76111022": {
        "Centro Poblado": "ALASKA"
    },
    "76111024": {
        "Centro Poblado": "LA PALOMERA"
    },
    "76111025": {
        "Centro Poblado": "LA UNIDAD"
    },
    "76111026": {
        "Centro Poblado": "PUERTO BERTIN"
    },
    "76111027": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76111029": {
        "Centro Poblado": "GUADUALEJO"
    },
    "76111030": {
        "Centro Poblado": "LA GRANJITA"
    },
    "76113000": {
        "Centro Poblado": "BUGALAGRANDE"
    },
    "76113001": {
        "Centro Poblado": "CEILÁN"
    },
    "76113004": {
        "Centro Poblado": "EL OVERO (SECTOR POBLADO)"
    },
    "76113008": {
        "Centro Poblado": "GALICIA"
    },
    "76113010": {
        "Centro Poblado": "MESTIZAL"
    },
    "76113011": {
        "Centro Poblado": "PAILA ARRIBA"
    },
    "76113013": {
        "Centro Poblado": "URÍBE URÍBE"
    },
    "76113016": {
        "Centro Poblado": "EL OVERO (SECTOR LA MARÍA)"
    },
    "76122000": {
        "Centro Poblado": "CAICEDONIA"
    },
    "76122006": {
        "Centro Poblado": "SAMARIA"
    },
    "76122009": {
        "Centro Poblado": "BARRAGÁN"
    },
    "76122010": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "76122011": {
        "Centro Poblado": "VILLA AURES"
    },
    "76126000": {
        "Centro Poblado": "DARIÉN"
    },
    "76126007": {
        "Centro Poblado": "LA GAVIOTA"
    },
    "76126018": {
        "Centro Poblado": "LA PLAYA"
    },
    "76130000": {
        "Centro Poblado": "CANDELARIA"
    },
    "76130001": {
        "Centro Poblado": "BUCHITOLO"
    },
    "76130002": {
        "Centro Poblado": "EL ARENAL"
    },
    "76130003": {
        "Centro Poblado": "EL CABUYAL"
    },
    "76130004": {
        "Centro Poblado": "EL CARMELO"
    },
    "76130005": {
        "Centro Poblado": "EL LAURO"
    },
    "76130006": {
        "Centro Poblado": "EL TIPLE"
    },
    "76130007": {
        "Centro Poblado": "JUANCHITO"
    },
    "76130008": {
        "Centro Poblado": "VILLA GORGONA"
    },
    "76130009": {
        "Centro Poblado": "LA REGINA"
    },
    "76130011": {
        "Centro Poblado": "MADRE VIEJA"
    },
    "76130012": {
        "Centro Poblado": "SAN JOAQUÍN"
    },
    "76130014": {
        "Centro Poblado": "EL OTOÑO"
    },
    "76130015": {
        "Centro Poblado": "EL GUALÍ"
    },
    "76130016": {
        "Centro Poblado": "EL POBLADO CAMPESTRE"
    },
    "76130017": {
        "Centro Poblado": "BRISAS DEL FRAILE"
    },
    "76130018": {
        "Centro Poblado": "CANTALOMOTA"
    },
    "76130019": {
        "Centro Poblado": "CAUCASECO"
    },
    "76130020": {
        "Centro Poblado": "DOMINGO LARGO"
    },
    "76130021": {
        "Centro Poblado": "LA ALBANIA"
    },
    "76130022": {
        "Centro Poblado": "LA GLORIA"
    },
    "76130023": {
        "Centro Poblado": "TRES TUSAS"
    },
    "76130027": {
        "Centro Poblado": "EL SILENCIO"
    },
    "76130038": {
        "Centro Poblado": "PATIO BONITO"
    },
    "76130039": {
        "Centro Poblado": "SAN ANDRESITO"
    },
    "76147000": {
        "Centro Poblado": "CARTAGO"
    },
    "76147005": {
        "Centro Poblado": "MODÍN"
    },
    "76147006": {
        "Centro Poblado": "PIEDRA DE MOLER"
    },
    "76147012": {
        "Centro Poblado": "GUANABANO"
    },
    "76147013": {
        "Centro Poblado": "GUAYABITO"
    },
    "76147014": {
        "Centro Poblado": "ZANJÓN CAUCA"
    },
    "76233000": {
        "Centro Poblado": "DAGUA"
    },
    "76233001": {
        "Centro Poblado": "ATUNCELA"
    },
    "76233002": {
        "Centro Poblado": "BORRERO AYERBE"
    },
    "76233004": {
        "Centro Poblado": "CISNEROS"
    },
    "76233005": {
        "Centro Poblado": "EL CARMEN"
    },
    "76233007": {
        "Centro Poblado": "EL LIMONAR"
    },
    "76233008": {
        "Centro Poblado": "EL NARANJO"
    },
    "76233009": {
        "Centro Poblado": "EL PALMAR"
    },
    "76233010": {
        "Centro Poblado": "EL PIÑAL"
    },
    "76233011": {
        "Centro Poblado": "EL QUEREMAL"
    },
    "76233012": {
        "Centro Poblado": "EL SALADO"
    },
    "76233017": {
        "Centro Poblado": "LOBO GUERRERO"
    },
    "76233019": {
        "Centro Poblado": "SAN BERNARDO"
    },
    "76233020": {
        "Centro Poblado": "SAN VICENTE"
    },
    "76233021": {
        "Centro Poblado": "SANTA MARÍA"
    },
    "76233023": {
        "Centro Poblado": "TOCOTÁ"
    },
    "76233025": {
        "Centro Poblado": "ZABALETAS"
    },
    "76233027": {
        "Centro Poblado": "JUNTAS"
    },
    "76233033": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "76233035": {
        "Centro Poblado": "EL CHILCAL"
    },
    "76233036": {
        "Centro Poblado": "KILÓMETRO 26"
    },
    "76233039": {
        "Centro Poblado": "LA VIRGEN"
    },
    "76233041": {
        "Centro Poblado": "LAS CAMELIAS"
    },
    "76233044": {
        "Centro Poblado": "VERGEL"
    },
    "76233045": {
        "Centro Poblado": "EL GALPÓN"
    },
    "76233046": {
        "Centro Poblado": "EL RODEO"
    },
    "76233047": {
        "Centro Poblado": "KATANGA"
    },
    "76233048": {
        "Centro Poblado": "EL CEDRO"
    },
    "76233049": {
        "Centro Poblado": "LA DELFINA"
    },
    "76233050": {
        "Centro Poblado": "EL EDEN"
    },
    "76233051": {
        "Centro Poblado": "PLAYA LARGA"
    },
    "76243000": {
        "Centro Poblado": "EL ÁGUILA"
    },
    "76243002": {
        "Centro Poblado": "LA ESPARTA"
    },
    "76243005": {
        "Centro Poblado": "LA MARÍA - QUEBRADAGRANDE"
    },
    "76243006": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "76243008": {
        "Centro Poblado": "CAÑAVERAL - VILLANUEVA"
    },
    "76243030": {
        "Centro Poblado": "LA QUIEBRA DE SAN PABLO"
    },
    "76243031": {
        "Centro Poblado": "EL GUAYABO"
    },
    "76246000": {
        "Centro Poblado": "EL CAIRO"
    },
    "76246001": {
        "Centro Poblado": "ALBÁN"
    },
    "76248000": {
        "Centro Poblado": "EL CERRITO"
    },
    "76248003": {
        "Centro Poblado": "EL CASTILLO"
    },
    "76248005": {
        "Centro Poblado": "EL PLACER"
    },
    "76248006": {
        "Centro Poblado": "EL POMO"
    },
    "76248008": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76248009": {
        "Centro Poblado": "SANTA ELENA"
    },
    "76248010": {
        "Centro Poblado": "SANTA LUISA"
    },
    "76248011": {
        "Centro Poblado": "TENERIFE"
    },
    "76248014": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "76248018": {
        "Centro Poblado": "LA HONDA"
    },
    "76250000": {
        "Centro Poblado": "EL DOVIO"
    },
    "76250003": {
        "Centro Poblado": "BITACO"
    },
    "76250007": {
        "Centro Poblado": "LITUANIA"
    },
    "76250013": {
        "Centro Poblado": "LA PRADERA"
    },
    "76250015": {
        "Centro Poblado": "MATECAÑA"
    },
    "76250016": {
        "Centro Poblado": "CAJAMARCA"
    },
    "76275000": {
        "Centro Poblado": "FLORIDA"
    },
    "76275004": {
        "Centro Poblado": "CHOCOCITO"
    },
    "76275006": {
        "Centro Poblado": "LA DIANA"
    },
    "76275010": {
        "Centro Poblado": "REMOLINO"
    },
    "76275011": {
        "Centro Poblado": "SAN ANTONIO DE LOS CABALLEROS"
    },
    "76275012": {
        "Centro Poblado": "SAN FRANCISCO (EL LLANITO)"
    },
    "76275014": {
        "Centro Poblado": "TARRAGONA"
    },
    "76275015": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "76275019": {
        "Centro Poblado": "LAS GUACAS"
    },
    "76275021": {
        "Centro Poblado": "LOS CALEÑOS"
    },
    "76275024": {
        "Centro Poblado": "EL INGENIO"
    },
    "76275025": {
        "Centro Poblado": "EL TAMBORAL"
    },
    "76275028": {
        "Centro Poblado": "SIMÓN BOLÍVAR"
    },
    "76306000": {
        "Centro Poblado": "GINEBRA"
    },
    "76306001": {
        "Centro Poblado": "COSTA RICA"
    },
    "76306002": {
        "Centro Poblado": "LA FLORESTA"
    },
    "76306005": {
        "Centro Poblado": "SABALETAS"
    },
    "76306008": {
        "Centro Poblado": "VILLA VANEGAS"
    },
    "76318000": {
        "Centro Poblado": "GUACARÍ"
    },
    "76318003": {
        "Centro Poblado": "GUABAS"
    },
    "76318004": {
        "Centro Poblado": "GUABITAS"
    },
    "76318006": {
        "Centro Poblado": "PICHICHÍ"
    },
    "76318007": {
        "Centro Poblado": "SANTA ROSA DE TAPIAS"
    },
    "76318008": {
        "Centro Poblado": "SONSO"
    },
    "76318009": {
        "Centro Poblado": "ALTO DE GUACAS"
    },
    "76318010": {
        "Centro Poblado": "PUENTE ROJO"
    },
    "76318011": {
        "Centro Poblado": "CANANGUÁ"
    },
    "76318012": {
        "Centro Poblado": "EL PLACER"
    },
    "76318013": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "76318014": {
        "Centro Poblado": "GUACAS"
    },
    "76364000": {
        "Centro Poblado": "JAMUNDÍ"
    },
    "76364001": {
        "Centro Poblado": "AMPUDIA"
    },
    "76364002": {
        "Centro Poblado": "BOCAS DEL PALO"
    },
    "76364003": {
        "Centro Poblado": "GUACHINTE"
    },
    "76364004": {
        "Centro Poblado": "LA LIBERIA"
    },
    "76364005": {
        "Centro Poblado": "PASO DE LA BOLSA"
    },
    "76364006": {
        "Centro Poblado": "POTRERITO"
    },
    "76364008": {
        "Centro Poblado": "PUENTE VÉLEZ"
    },
    "76364009": {
        "Centro Poblado": "QUINAMAYO"
    },
    "76364010": {
        "Centro Poblado": "ROBLES"
    },
    "76364011": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76364012": {
        "Centro Poblado": "SAN VICENTE"
    },
    "76364013": {
        "Centro Poblado": "TIMBA"
    },
    "76364014": {
        "Centro Poblado": "VILLA COLOMBIA"
    },
    "76364015": {
        "Centro Poblado": "VILLAPAZ"
    },
    "76364016": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "76364018": {
        "Centro Poblado": "LA MESETA"
    },
    "76364019": {
        "Centro Poblado": "LA VENTURA"
    },
    "76364021": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "76364022": {
        "Centro Poblado": "EL GUAVAL"
    },
    "76364023": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "76364024": {
        "Centro Poblado": "CASCARILLAL"
    },
    "76364026": {
        "Centro Poblado": "GATO DE MONTE"
    },
    "76364032": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "76364036": {
        "Centro Poblado": "CONDOMINIO"
    },
    "76377000": {
        "Centro Poblado": "LA CUMBRE"
    },
    "76377001": {
        "Centro Poblado": "BITACO"
    },
    "76377002": {
        "Centro Poblado": "LA MARÍA"
    },
    "76377003": {
        "Centro Poblado": "LOMITAS"
    },
    "76377004": {
        "Centro Poblado": "PAVAS"
    },
    "76377005": {
        "Centro Poblado": "PUENTE PALO"
    },
    "76377008": {
        "Centro Poblado": "ARBOLEDAS"
    },
    "76377009": {
        "Centro Poblado": "JIGUALES"
    },
    "76377010": {
        "Centro Poblado": "PAVITAS"
    },
    "76377011": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "76377012": {
        "Centro Poblado": "LA VENTURA"
    },
    "76400000": {
        "Centro Poblado": "LA UNIÓN"
    },
    "76400005": {
        "Centro Poblado": "QUEBRADA GRANDE"
    },
    "76400006": {
        "Centro Poblado": "SAN LUIS"
    },
    "76400008": {
        "Centro Poblado": "SABANAZO"
    },
    "76400009": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "76400010": {
        "Centro Poblado": "EL GUASIMO"
    },
    "76400011": {
        "Centro Poblado": "EL LUCERO"
    },
    "76400012": {
        "Centro Poblado": "LA CAMPESINA"
    },
    "76400013": {
        "Centro Poblado": "PÁJARO DE ORO"
    },
    "76403000": {
        "Centro Poblado": "LA VICTORIA"
    },
    "76403003": {
        "Centro Poblado": "HOLGUÍN"
    },
    "76403004": {
        "Centro Poblado": "MIRAVALLES"
    },
    "76403005": {
        "Centro Poblado": "RIVERALTA"
    },
    "76403006": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "76403007": {
        "Centro Poblado": "SAN PEDRO"
    },
    "76403009": {
        "Centro Poblado": "TAGUALES"
    },
    "76497000": {
        "Centro Poblado": "OBANDO"
    },
    "76497001": {
        "Centro Poblado": "CRUCES"
    },
    "76497002": {
        "Centro Poblado": "EL CHUZO"
    },
    "76497003": {
        "Centro Poblado": "JUAN DÍAZ"
    },
    "76497005": {
        "Centro Poblado": "PUERTO MOLINA"
    },
    "76497006": {
        "Centro Poblado": "PUERTO SAMARIA"
    },
    "76497007": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "76497008": {
        "Centro Poblado": "VILLA RODAS"
    },
    "76520000": {
        "Centro Poblado": "PALMIRA"
    },
    "76520001": {
        "Centro Poblado": "AGUACLARA"
    },
    "76520002": {
        "Centro Poblado": "AMAIME"
    },
    "76520004": {
        "Centro Poblado": "BARRANCAS"
    },
    "76520005": {
        "Centro Poblado": "BOLO ALIZAL"
    },
    "76520006": {
        "Centro Poblado": "BOLO LA ITALIA"
    },
    "76520007": {
        "Centro Poblado": "BOLO SAN ISIDRO"
    },
    "76520008": {
        "Centro Poblado": "BOYACÁ"
    },
    "76520009": {
        "Centro Poblado": "CALUCE - PLAN DE VIVIENDA LOS GUAYABOS"
    },
    "76520010": {
        "Centro Poblado": "CAUCASECO"
    },
    "76520011": {
        "Centro Poblado": "COMBIA"
    },
    "76520013": {
        "Centro Poblado": "CHONTADURO"
    },
    "76520014": {
        "Centro Poblado": "GUANABANAL"
    },
    "76520015": {
        "Centro Poblado": "GUAYABAL"
    },
    "76520016": {
        "Centro Poblado": "JUANCHITO"
    },
    "76520017": {
        "Centro Poblado": "LA ACEQUIA"
    },
    "76520018": {
        "Centro Poblado": "LA HERRADURA"
    },
    "76520019": {
        "Centro Poblado": "LA QUISQUINA"
    },
    "76520020": {
        "Centro Poblado": "LA TORRE"
    },
    "76520022": {
        "Centro Poblado": "MATAPALO"
    },
    "76520023": {
        "Centro Poblado": "OBANDO"
    },
    "76520024": {
        "Centro Poblado": "PALMASECA"
    },
    "76520025": {
        "Centro Poblado": "POTRERILLO"
    },
    "76520026": {
        "Centro Poblado": "ROZO"
    },
    "76520027": {
        "Centro Poblado": "TABLONES"
    },
    "76520028": {
        "Centro Poblado": "TENJO"
    },
    "76520029": {
        "Centro Poblado": "TIENDA NUEVA"
    },
    "76520032": {
        "Centro Poblado": "LA BUITRERA"
    },
    "76520033": {
        "Centro Poblado": "LA PAMPA"
    },
    "76520035": {
        "Centro Poblado": "LA BOLSA"
    },
    "76520038": {
        "Centro Poblado": "LA DOLORES"
    },
    "76520039": {
        "Centro Poblado": "LA CASCADA"
    },
    "76520041": {
        "Centro Poblado": "BOLO BARRIO NUEVO"
    },
    "76520043": {
        "Centro Poblado": "BOLOMADRE VIEJA"
    },
    "76520044": {
        "Centro Poblado": "LA UNION"
    },
    "76520045": {
        "Centro Poblado": "PILES"
    },
    "76520047": {
        "Centro Poblado": "SAN ANTONIO DE LAS PALMAS"
    },
    "76520048": {
        "Centro Poblado": "TRES TUSAS"
    },
    "76520049": {
        "Centro Poblado": "BOLO ITALIA 1"
    },
    "76520050": {
        "Centro Poblado": "BOLO ITALIA 2"
    },
    "76520051": {
        "Centro Poblado": "CONDOMINIO CAMPESTRE LA GONZALEZ"
    },
    "76520052": {
        "Centro Poblado": "LA BUITRERA 1"
    },
    "76520053": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "76563000": {
        "Centro Poblado": "PRADERA"
    },
    "76563011": {
        "Centro Poblado": "LA GRANJA"
    },
    "76563013": {
        "Centro Poblado": "LA TUPIA"
    },
    "76563014": {
        "Centro Poblado": "LOMITAS"
    },
    "76563018": {
        "Centro Poblado": "POTRERITO"
    },
    "76563024": {
        "Centro Poblado": "EL RECREO"
    },
    "76563025": {
        "Centro Poblado": "LA FERIA"
    },
    "76563028": {
        "Centro Poblado": "LA CRUZ"
    },
    "76606000": {
        "Centro Poblado": "RESTREPO"
    },
    "76606008": {
        "Centro Poblado": "SAN SALVADOR"
    },
    "76606016": {
        "Centro Poblado": "BARRIO LA INDEPENDENCIA"
    },
    "76616000": {
        "Centro Poblado": "RIOFRÍO"
    },
    "76616002": {
        "Centro Poblado": "FENICIA"
    },
    "76616003": {
        "Centro Poblado": "PALMA - LA CUCHILLA"
    },
    "76616005": {
        "Centro Poblado": "LA ZULIA"
    },
    "76616006": {
        "Centro Poblado": "MADRIGAL"
    },
    "76616007": {
        "Centro Poblado": "PORTUGAL DE PIEDRAS"
    },
    "76616009": {
        "Centro Poblado": "SALÓNICA"
    },
    "76616010": {
        "Centro Poblado": "EL JAGUAL"
    },
    "76616013": {
        "Centro Poblado": "PUERTO FENICIA"
    },
    "76616014": {
        "Centro Poblado": "LOS ALPES"
    },
    "76616015": {
        "Centro Poblado": "LA SULTANA"
    },
    "76616016": {
        "Centro Poblado": "LAS BRISAS"
    },
    "76616017": {
        "Centro Poblado": "LOS ESTRECHOS"
    },
    "76622000": {
        "Centro Poblado": "ROLDANILLO"
    },
    "76622002": {
        "Centro Poblado": "EL RETIRO"
    },
    "76622003": {
        "Centro Poblado": "HIGUERONCITO"
    },
    "76622007": {
        "Centro Poblado": "MORELIA"
    },
    "76622009": {
        "Centro Poblado": "SANTA RITA"
    },
    "76622020": {
        "Centro Poblado": "PALMAR GUAYABAL"
    },
    "76622022": {
        "Centro Poblado": "TIERRA BLANCA"
    },
    "76670000": {
        "Centro Poblado": "SAN PEDRO"
    },
    "76670002": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "76670007": {
        "Centro Poblado": "PRESIDENTE"
    },
    "76670008": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "76670009": {
        "Centro Poblado": "TODOS LOS SANTOS"
    },
    "76670010": {
        "Centro Poblado": "GUAYABAL"
    },
    "76670011": {
        "Centro Poblado": "MONTE GRANDE"
    },
    "76736000": {
        "Centro Poblado": "SEVILLA"
    },
    "76736004": {
        "Centro Poblado": "COROZAL"
    },
    "76736005": {
        "Centro Poblado": "CUMBARCO"
    },
    "76736008": {
        "Centro Poblado": "LA CUCHILLA"
    },
    "76736014": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76736018": {
        "Centro Poblado": "QUEBRADANUEVA"
    },
    "76736030": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "76823000": {
        "Centro Poblado": "TORO"
    },
    "76823001": {
        "Centro Poblado": "BOHÍO"
    },
    "76823006": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "76823007": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "76823008": {
        "Centro Poblado": "LA QUIEBRA"
    },
    "76828000": {
        "Centro Poblado": "TRUJILLO"
    },
    "76828002": {
        "Centro Poblado": "ANDINÁPOLIS"
    },
    "76828003": {
        "Centro Poblado": "CRISTALES"
    },
    "76828004": {
        "Centro Poblado": "DOS QUEBRADAS"
    },
    "76828006": {
        "Centro Poblado": "HUASANÓ"
    },
    "76828007": {
        "Centro Poblado": "ROBLEDO"
    },
    "76828008": {
        "Centro Poblado": "SAN ISIDRO"
    },
    "76828010": {
        "Centro Poblado": "VENECIA"
    },
    "76828013": {
        "Centro Poblado": "LA SONORA"
    },
    "76834000": {
        "Centro Poblado": "TULUÁ"
    },
    "76834001": {
        "Centro Poblado": "AGUACLARA"
    },
    "76834003": {
        "Centro Poblado": "BARRAGÁN"
    },
    "76834004": {
        "Centro Poblado": "BOCAS DE TULUÁ"
    },
    "76834005": {
        "Centro Poblado": "EL PICACHO"
    },
    "76834007": {
        "Centro Poblado": "PUERTO FRAZADAS"
    },
    "76834009": {
        "Centro Poblado": "LA IBERIA"
    },
    "76834010": {
        "Centro Poblado": "LA MARINA"
    },
    "76834011": {
        "Centro Poblado": "LA MORALIA"
    },
    "76834012": {
        "Centro Poblado": "LA PALMERA"
    },
    "76834015": {
        "Centro Poblado": "MONTELORO"
    },
    "76834016": {
        "Centro Poblado": "NARIÑO"
    },
    "76834021": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "76834023": {
        "Centro Poblado": "TRES ESQUINAS"
    },
    "76834025": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "76834026": {
        "Centro Poblado": "LA RIVERA"
    },
    "76834029": {
        "Centro Poblado": "CIENEGUETA"
    },
    "76834030": {
        "Centro Poblado": "GATO NEGRO"
    },
    "76834032": {
        "Centro Poblado": "PALOMESTIZO"
    },
    "76834033": {
        "Centro Poblado": "LA COLINA"
    },
    "76845000": {
        "Centro Poblado": "ULLOA"
    },
    "76845002": {
        "Centro Poblado": "MOCTEZUMA"
    },
    "76845005": {
        "Centro Poblado": "DINAMARCA"
    },
    "76863000": {
        "Centro Poblado": "VERSALLES"
    },
    "76863001": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "76863002": {
        "Centro Poblado": "EL BALSAL"
    },
    "76863007": {
        "Centro Poblado": "LA FLORIDA"
    },
    "76863012": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "76863014": {
        "Centro Poblado": "MURRAPAL"
    },
    "76863017": {
        "Centro Poblado": "LA PLAYA"
    },
    "76863019": {
        "Centro Poblado": "LA CABAÑA"
    },
    "76869000": {
        "Centro Poblado": "VIJES"
    },
    "76869001": {
        "Centro Poblado": "CACHIMBAL"
    },
    "76869003": {
        "Centro Poblado": "EL PORVENIR"
    },
    "76869004": {
        "Centro Poblado": "LA FRESNEDA"
    },
    "76869007": {
        "Centro Poblado": "LA RIVERA"
    },
    "76869008": {
        "Centro Poblado": "EL TAMBOR"
    },
    "76869010": {
        "Centro Poblado": "VIDAL"
    },
    "76890000": {
        "Centro Poblado": "YOTOCO"
    },
    "76890001": {
        "Centro Poblado": "EL CANEY"
    },
    "76890003": {
        "Centro Poblado": "JIGUALES"
    },
    "76890004": {
        "Centro Poblado": "RAYITO"
    },
    "76890005": {
        "Centro Poblado": "LAS DELICIAS"
    },
    "76890006": {
        "Centro Poblado": "MEDIACANOA"
    },
    "76890007": {
        "Centro Poblado": "MIRAVALLE"
    },
    "76890008": {
        "Centro Poblado": "PUENTETIERRA"
    },
    "76890009": {
        "Centro Poblado": "SAN ANTONIO DE PIEDRAS"
    },
    "76890011": {
        "Centro Poblado": "CAMPOALEGRE"
    },
    "76890013": {
        "Centro Poblado": "LOS PLANES"
    },
    "76890014": {
        "Centro Poblado": "PUNTA BRAVA"
    },
    "76892000": {
        "Centro Poblado": "YUMBO"
    },
    "76892002": {
        "Centro Poblado": "DAPA LA VEGA"
    },
    "76892004": {
        "Centro Poblado": "MONTAÑITAS"
    },
    "76892005": {
        "Centro Poblado": "MULALÓ"
    },
    "76892008": {
        "Centro Poblado": "SAN MARCOS"
    },
    "76892009": {
        "Centro Poblado": "SANTA INÉS"
    },
    "76892013": {
        "Centro Poblado": "DAPA EL RINCÓN"
    },
    "76892014": {
        "Centro Poblado": "EL PEDREGAL"
    },
    "76892015": {
        "Centro Poblado": "MIRAVALLE NORTE"
    },
    "76892017": {
        "Centro Poblado": "ARROYOHONDO"
    },
    "76892018": {
        "Centro Poblado": "EL CHOCHO"
    },
    "76892019": {
        "Centro Poblado": "MANGA VIEJA"
    },
    "76892020": {
        "Centro Poblado": "MIRAVALLE DAPA"
    },
    "76892021": {
        "Centro Poblado": "PILAS DE DAPA"
    },
    "76895000": {
        "Centro Poblado": "ZARZAL"
    },
    "76895002": {
        "Centro Poblado": "LA PAILA"
    },
    "76895003": {
        "Centro Poblado": "LIMONES"
    },
    "76895004": {
        "Centro Poblado": "QUEBRADANUEVA"
    },
    "76895005": {
        "Centro Poblado": "VALLEJUELO"
    },
    "76895008": {
        "Centro Poblado": "ESTACIÓN CAICEDONIA"
    },
    "81001000": {
        "Centro Poblado": "ARAUCA"
    },
    "81001001": {
        "Centro Poblado": "CLARINETERO"
    },
    "81001017": {
        "Centro Poblado": "EL CARACOL"
    },
    "81001020": {
        "Centro Poblado": "MONSERRATE"
    },
    "81001021": {
        "Centro Poblado": "LAS NUBES"
    },
    "81001022": {
        "Centro Poblado": "MANHATAN"
    },
    "81065000": {
        "Centro Poblado": "ARAUQUITA"
    },
    "81065001": {
        "Centro Poblado": "CARRETERO"
    },
    "81065002": {
        "Centro Poblado": "EL TRONCAL"
    },
    "81065004": {
        "Centro Poblado": "SAN LORENZO"
    },
    "81065005": {
        "Centro Poblado": "LA PAZ"
    },
    "81065007": {
        "Centro Poblado": "LA REINERA (GAVIOTA)"
    },
    "81065008": {
        "Centro Poblado": "LA ESMERALDA (JUJUA)"
    },
    "81065009": {
        "Centro Poblado": "AGUACHICA"
    },
    "81065010": {
        "Centro Poblado": "EL CAUCHO"
    },
    "81065016": {
        "Centro Poblado": "LOS CHORROS"
    },
    "81065017": {
        "Centro Poblado": "PANAMÁ DE ARAUCA"
    },
    "81065019": {
        "Centro Poblado": "BRISAS DEL CARANAL"
    },
    "81065020": {
        "Centro Poblado": "EL OASIS"
    },
    "81065021": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "81065022": {
        "Centro Poblado": "LA PESQUERA"
    },
    "81065023": {
        "Centro Poblado": "EL CAMPAMENTO"
    },
    "81065025": {
        "Centro Poblado": "ARENOSA"
    },
    "81065026": {
        "Centro Poblado": "BOCAS DEL ELE"
    },
    "81065027": {
        "Centro Poblado": "CAÑO HONDO"
    },
    "81065028": {
        "Centro Poblado": "EL CAMPING"
    },
    "81065029": {
        "Centro Poblado": "FILIPINAS"
    },
    "81065030": {
        "Centro Poblado": "JARDINES"
    },
    "81065031": {
        "Centro Poblado": "LOS COLONOS"
    },
    "81065032": {
        "Centro Poblado": "MATECAÑA"
    },
    "81065033": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "81065034": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "81065038": {
        "Centro Poblado": "LA PRIMAVERA"
    },
    "81065039": {
        "Centro Poblado": "SANTA ANA"
    },
    "81220000": {
        "Centro Poblado": "CRAVO NORTE"
    },
    "81300000": {
        "Centro Poblado": "FORTUL"
    },
    "81300002": {
        "Centro Poblado": "CARANAL"
    },
    "81300003": {
        "Centro Poblado": "LA VEINTE"
    },
    "81300006": {
        "Centro Poblado": "EL MORDISCO"
    },
    "81300007": {
        "Centro Poblado": "PALMARITO"
    },
    "81300009": {
        "Centro Poblado": "SITIO NUEVO"
    },
    "81300011": {
        "Centro Poblado": "TOLUA"
    },
    "81591000": {
        "Centro Poblado": "PUERTO RONDÓN"
    },
    "81591006": {
        "Centro Poblado": "SAN IGNACIO"
    },
    "81736000": {
        "Centro Poblado": "SARAVENA"
    },
    "81736002": {
        "Centro Poblado": "LA YE DEL CHARO"
    },
    "81736006": {
        "Centro Poblado": "PUERTO LLERAS"
    },
    "81736007": {
        "Centro Poblado": "AGUA SANTA"
    },
    "81736008": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "81736009": {
        "Centro Poblado": "BARRANCONES"
    },
    "81736010": {
        "Centro Poblado": "BARRIO LOCO"
    },
    "81736011": {
        "Centro Poblado": "CAÑO SECO"
    },
    "81736012": {
        "Centro Poblado": "LA PAJUILA"
    },
    "81736013": {
        "Centro Poblado": "LA YE DEL GARROTAZO"
    },
    "81736014": {
        "Centro Poblado": "PUERTO CONTRERAS"
    },
    "81736017": {
        "Centro Poblado": "REMOLINO"
    },
    "81794000": {
        "Centro Poblado": "TAME"
    },
    "81794001": {
        "Centro Poblado": "BETOYES"
    },
    "81794004": {
        "Centro Poblado": "COROCITO"
    },
    "81794006": {
        "Centro Poblado": "PUERTO GAITÁN"
    },
    "81794009": {
        "Centro Poblado": "PUERTO SAN SALVADOR"
    },
    "81794014": {
        "Centro Poblado": "LA HOLANDA"
    },
    "81794015": {
        "Centro Poblado": "PUENTE TABLA"
    },
    "81794019": {
        "Centro Poblado": "BOTALÓN"
    },
    "81794020": {
        "Centro Poblado": "PUERTO MIRANDA"
    },
    "81794021": {
        "Centro Poblado": "ALTO CAUCA"
    },
    "81794022": {
        "Centro Poblado": "FLOR AMARILLO"
    },
    "81794024": {
        "Centro Poblado": "LAS MALVINAS"
    },
    "81794026": {
        "Centro Poblado": "PUEBLO SECO"
    },
    "81794027": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "81794028": {
        "Centro Poblado": "PUEBLO SUCIO"
    },
    "85001000": {
        "Centro Poblado": "YOPAL"
    },
    "85001001": {
        "Centro Poblado": "EL MORRO"
    },
    "85001002": {
        "Centro Poblado": "LA CHAPARRERA"
    },
    "85001003": {
        "Centro Poblado": "TILODIRÁN"
    },
    "85001005": {
        "Centro Poblado": "EL CHARTE"
    },
    "85001006": {
        "Centro Poblado": "SANTAFÉ DE MORICHAL"
    },
    "85001007": {
        "Centro Poblado": "QUEBRADA SECA"
    },
    "85001010": {
        "Centro Poblado": "LA GUAFILLA"
    },
    "85001011": {
        "Centro Poblado": "LA LLANERITA"
    },
    "85001012": {
        "Centro Poblado": "LA NIATA"
    },
    "85001013": {
        "Centro Poblado": "PUNTO NUEVO"
    },
    "85001014": {
        "Centro Poblado": "LA VEGA"
    },
    "85010000": {
        "Centro Poblado": "AGUAZUL"
    },
    "85010001": {
        "Centro Poblado": "CUPIAGUA"
    },
    "85010002": {
        "Centro Poblado": "MONTERRALO"
    },
    "85010003": {
        "Centro Poblado": "SAN BENITO"
    },
    "85010005": {
        "Centro Poblado": "SAN JOSÉ"
    },
    "85010006": {
        "Centro Poblado": "UNETE"
    },
    "85010010": {
        "Centro Poblado": "PUENTE CUSIANA"
    },
    "85010014": {
        "Centro Poblado": "LLANO LINDO"
    },
    "85010015": {
        "Centro Poblado": "PLAN BRISAS"
    },
    "85010016": {
        "Centro Poblado": "ATALAYAS"
    },
    "85015000": {
        "Centro Poblado": "CHÁMEZA"
    },
    "85125000": {
        "Centro Poblado": "HATO COROZAL"
    },
    "85125002": {
        "Centro Poblado": "CHIRE"
    },
    "85125003": {
        "Centro Poblado": "LA FRONTERA - LA CHAPA"
    },
    "85125005": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "85125010": {
        "Centro Poblado": "SANTA RITA"
    },
    "85125011": {
        "Centro Poblado": "SAN JOSÉ DE ARIPORO"
    },
    "85125016": {
        "Centro Poblado": "ROSA BLANCA"
    },
    "85125017": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "85125018": {
        "Centro Poblado": "CAÑO MOCHUELO"
    },
    "85136000": {
        "Centro Poblado": "LA SALINA"
    },
    "85139000": {
        "Centro Poblado": "MANÍ"
    },
    "85139001": {
        "Centro Poblado": "GUAFALPINTADO"
    },
    "85139003": {
        "Centro Poblado": "GAVIOTAS"
    },
    "85139005": {
        "Centro Poblado": "SANTA HELENA DE CÚSIVA"
    },
    "85139007": {
        "Centro Poblado": "CHAVINAVE"
    },
    "85162000": {
        "Centro Poblado": "MONTERREY"
    },
    "85162001": {
        "Centro Poblado": "PALONEGRO"
    },
    "85162002": {
        "Centro Poblado": "BRISAS DE LLANO"
    },
    "85162004": {
        "Centro Poblado": "EL PORVENIR"
    },
    "85162006": {
        "Centro Poblado": "VILLA CAROLA"
    },
    "85162007": {
        "Centro Poblado": "LA HORQUETA"
    },
    "85162008": {
        "Centro Poblado": "LA ESTRELLA"
    },
    "85162009": {
        "Centro Poblado": "PORVENIR SECTOR LA 40"
    },
    "85225000": {
        "Centro Poblado": "NUNCHÍA"
    },
    "85225016": {
        "Centro Poblado": "LA YOPALOSA"
    },
    "85230000": {
        "Centro Poblado": "OROCUÉ"
    },
    "85230003": {
        "Centro Poblado": "EL ALGARROBO"
    },
    "85230011": {
        "Centro Poblado": "CARRIZALES"
    },
    "85230012": {
        "Centro Poblado": "DUYA (RESGUARDO)"
    },
    "85250000": {
        "Centro Poblado": "PAZ DE ARIPORO"
    },
    "85250001": {
        "Centro Poblado": "BOCAS DE LA HERMOSA"
    },
    "85250002": {
        "Centro Poblado": "CENTRO GAITÁN"
    },
    "85250003": {
        "Centro Poblado": "CAÑO CHIQUITO"
    },
    "85250004": {
        "Centro Poblado": "LA AGUADA"
    },
    "85250006": {
        "Centro Poblado": "MONTAÑA DEL TOTUMO"
    },
    "85250007": {
        "Centro Poblado": "LAS GUAMAS"
    },
    "85250008": {
        "Centro Poblado": "RINCÓN HONDO"
    },
    "85263000": {
        "Centro Poblado": "PORE"
    },
    "85263001": {
        "Centro Poblado": "EL BANCO"
    },
    "85263002": {
        "Centro Poblado": "LA PLATA"
    },
    "85279000": {
        "Centro Poblado": "RECETOR"
    },
    "85279002": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "85300000": {
        "Centro Poblado": "SABANALARGA"
    },
    "85300001": {
        "Centro Poblado": "AGUACLARA"
    },
    "85300003": {
        "Centro Poblado": "EL SECRETO"
    },
    "85315000": {
        "Centro Poblado": "SÁCAMA"
    },
    "85325000": {
        "Centro Poblado": "SAN LUIS DE PALENQUE"
    },
    "85325002": {
        "Centro Poblado": "MIRAMAR DE GUANAPALO"
    },
    "85325004": {
        "Centro Poblado": "EL PALMAR DE GUANAPALO"
    },
    "85325005": {
        "Centro Poblado": "JAGUEYES"
    },
    "85400000": {
        "Centro Poblado": "TÁMARA"
    },
    "85400002": {
        "Centro Poblado": "TABLÓN DE TAMARA"
    },
    "85400004": {
        "Centro Poblado": "TEISLANDIA"
    },
    "85410000": {
        "Centro Poblado": "TAURAMENA"
    },
    "85410003": {
        "Centro Poblado": "CARUPANA"
    },
    "85410004": {
        "Centro Poblado": "TUNUPE"
    },
    "85410005": {
        "Centro Poblado": "PASO CUSIANA"
    },
    "85410006": {
        "Centro Poblado": "RAIZAL"
    },
    "85410007": {
        "Centro Poblado": "ACEITE ALTO"
    },
    "85430000": {
        "Centro Poblado": "TRINIDAD"
    },
    "85430001": {
        "Centro Poblado": "BOCAS DEL PAUTO"
    },
    "85430007": {
        "Centro Poblado": "EL CONVENTO"
    },
    "85430008": {
        "Centro Poblado": "SANTA IRENE"
    },
    "85440000": {
        "Centro Poblado": "VILLANUEVA"
    },
    "85440001": {
        "Centro Poblado": "CARIBAYONA"
    },
    "85440002": {
        "Centro Poblado": "SANTA HELENA DE UPÍA"
    },
    "85440003": {
        "Centro Poblado": "SAN AGUSTÍN"
    },
    "85440005": {
        "Centro Poblado": "BANQUETAS"
    },
    "85440006": {
        "Centro Poblado": "LOMA LINDA"
    },
    "85440007": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "86001000": {
        "Centro Poblado": "MOCOA"
    },
    "86001002": {
        "Centro Poblado": "EL PEPINO"
    },
    "86001003": {
        "Centro Poblado": "PUEBLO VIEJO"
    },
    "86001004": {
        "Centro Poblado": "PUERTO LIMÓN"
    },
    "86001006": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "86001009": {
        "Centro Poblado": "YUNGUILLO"
    },
    "86001014": {
        "Centro Poblado": "LA TEBAIDA"
    },
    "86001016": {
        "Centro Poblado": "ALTO AFAN"
    },
    "86001017": {
        "Centro Poblado": "BRISAS DEL SOL"
    },
    "86001018": {
        "Centro Poblado": "PLANADAS"
    },
    "86001019": {
        "Centro Poblado": "RUMIYACO"
    },
    "86001020": {
        "Centro Poblado": "SAN ANTONIO 2"
    },
    "86001021": {
        "Centro Poblado": "LA RESERVA"
    },
    "86001022": {
        "Centro Poblado": "SAN JOSÉ DEL PEPINO"
    },
    "86219000": {
        "Centro Poblado": "COLÓN"
    },
    "86219001": {
        "Centro Poblado": "SAN PEDRO"
    },
    "86219002": {
        "Centro Poblado": "LAS PALMAS"
    },
    "86219003": {
        "Centro Poblado": "MICHUACAN"
    },
    "86320000": {
        "Centro Poblado": "ORITO"
    },
    "86320001": {
        "Centro Poblado": "TESALIA"
    },
    "86320004": {
        "Centro Poblado": "LUCITANIA"
    },
    "86320008": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "86320009": {
        "Centro Poblado": "SAN VICENTE DE LUZÓN"
    },
    "86320010": {
        "Centro Poblado": "SIBERIA"
    },
    "86320011": {
        "Centro Poblado": "SIMÓN BOLÍVAR"
    },
    "86320013": {
        "Centro Poblado": "EL ACHIOTE"
    },
    "86320014": {
        "Centro Poblado": "EL LÍBANO"
    },
    "86320015": {
        "Centro Poblado": "EL PARAISO"
    },
    "86320016": {
        "Centro Poblado": "EL YARUMO"
    },
    "86320017": {
        "Centro Poblado": "MONSERRATE"
    },
    "86568000": {
        "Centro Poblado": "PUERTO ASÍS"
    },
    "86568006": {
        "Centro Poblado": "PIÑUÑA BLANCO"
    },
    "86568019": {
        "Centro Poblado": "SANTANA"
    },
    "86568020": {
        "Centro Poblado": "PUERTO VEGA"
    },
    "86568021": {
        "Centro Poblado": "TETEYE"
    },
    "86568023": {
        "Centro Poblado": "CAÑA BRAVA"
    },
    "86568026": {
        "Centro Poblado": "LA CARMELITA"
    },
    "86568027": {
        "Centro Poblado": "LA LIBERTAD"
    },
    "86568029": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "86568031": {
        "Centro Poblado": "SINAÍ (ACHAPOS)"
    },
    "86568032": {
        "Centro Poblado": "BRISAS DEL HONG KONG"
    },
    "86568033": {
        "Centro Poblado": "LA CABAÑA"
    },
    "86568034": {
        "Centro Poblado": "PLANADAS"
    },
    "86568035": {
        "Centro Poblado": "EL MUELLE"
    },
    "86569000": {
        "Centro Poblado": "PUERTO CAICEDO"
    },
    "86569001": {
        "Centro Poblado": "SAN PEDRO"
    },
    "86569002": {
        "Centro Poblado": "VILLA FLOR"
    },
    "86569003": {
        "Centro Poblado": "EL CEDRAL"
    },
    "86569004": {
        "Centro Poblado": "EL VENADO"
    },
    "86569005": {
        "Centro Poblado": "LAS VEGAS"
    },
    "86571000": {
        "Centro Poblado": "PUERTO GUZMÁN"
    },
    "86571001": {
        "Centro Poblado": "EL CEDRO"
    },
    "86571002": {
        "Centro Poblado": "SANTA LUCÍA"
    },
    "86571003": {
        "Centro Poblado": "JOSÉ MARÍA"
    },
    "86571004": {
        "Centro Poblado": "MAYOYOGUE"
    },
    "86571005": {
        "Centro Poblado": "EL GALLINAZO"
    },
    "86571006": {
        "Centro Poblado": "SAN ROQUE"
    },
    "86571007": {
        "Centro Poblado": "EL JUANO"
    },
    "86571008": {
        "Centro Poblado": "PUERTO ROSARIO"
    },
    "86571009": {
        "Centro Poblado": "GALILEA"
    },
    "86571010": {
        "Centro Poblado": "EL RECREO"
    },
    "86571011": {
        "Centro Poblado": "EL BOMBON"
    },
    "86571012": {
        "Centro Poblado": "EL MUELLE"
    },
    "86571013": {
        "Centro Poblado": "LA PATRIA"
    },
    "86571014": {
        "Centro Poblado": "LOS GUADUALES"
    },
    "86571015": {
        "Centro Poblado": "LA CIUDADELA"
    },
    "86573000": {
        "Centro Poblado": "PUERTO LEGUÍZAMO"
    },
    "86573001": {
        "Centro Poblado": "LA TAGUA"
    },
    "86573002": {
        "Centro Poblado": "PUERTO OSPINA"
    },
    "86573003": {
        "Centro Poblado": "SENSELLA"
    },
    "86573005": {
        "Centro Poblado": "EL MECAYA"
    },
    "86573009": {
        "Centro Poblado": "PIÑUÑA NEGRO"
    },
    "86573010": {
        "Centro Poblado": "NUEVA APAYA"
    },
    "86573011": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "86749000": {
        "Centro Poblado": "SIBUNDOY"
    },
    "86749008": {
        "Centro Poblado": "SAGRADO CORAZON DE JESUS"
    },
    "86749009": {
        "Centro Poblado": "LAS COCHAS"
    },
    "86749010": {
        "Centro Poblado": "VILLA FLOR"
    },
    "86755000": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "86755001": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "86755003": {
        "Centro Poblado": "SAN SILVESTRE"
    },
    "86755004": {
        "Centro Poblado": "MINCHOY"
    },
    "86757000": {
        "Centro Poblado": "LA DORADA"
    },
    "86757001": {
        "Centro Poblado": "PUERTO COLÓN"
    },
    "86757004": {
        "Centro Poblado": "AGUA BLANCA"
    },
    "86757013": {
        "Centro Poblado": "EL CHIGUACO"
    },
    "86757015": {
        "Centro Poblado": "EL MAIZAL"
    },
    "86757018": {
        "Centro Poblado": "JORDÁN ORTÍZ"
    },
    "86757019": {
        "Centro Poblado": "LA CABAÑA"
    },
    "86757025": {
        "Centro Poblado": "LA GUISITA"
    },
    "86757028": {
        "Centro Poblado": "MESAS DEL SABALITO"
    },
    "86757032": {
        "Centro Poblado": "NUEVA RISARALDA"
    },
    "86757043": {
        "Centro Poblado": "SAN LUIS DE LA FRONTERA"
    },
    "86757049": {
        "Centro Poblado": "EL PARAISO"
    },
    "86757050": {
        "Centro Poblado": "LA INVASIÓN"
    },
    "86757051": {
        "Centro Poblado": "LOS UVOS"
    },
    "86760000": {
        "Centro Poblado": "SANTIAGO"
    },
    "86760001": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "86865000": {
        "Centro Poblado": "LA HORMIGA"
    },
    "86865003": {
        "Centro Poblado": "EL TIGRE"
    },
    "86865004": {
        "Centro Poblado": "EL PLACER"
    },
    "86865005": {
        "Centro Poblado": "SAN ANTONIO"
    },
    "86865008": {
        "Centro Poblado": "JORDÁN DE GUISIA"
    },
    "86865010": {
        "Centro Poblado": "BRISAS DEL PALMAR"
    },
    "86865011": {
        "Centro Poblado": "EL CAIRO"
    },
    "86865012": {
        "Centro Poblado": "EL VENADO"
    },
    "86865014": {
        "Centro Poblado": "LA CONCORDIA"
    },
    "86865015": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "86865016": {
        "Centro Poblado": "LORO UNO"
    },
    "86865018": {
        "Centro Poblado": "NUEVA PALESTINA"
    },
    "86865019": {
        "Centro Poblado": "SAN ANDRÉS"
    },
    "86865021": {
        "Centro Poblado": "VILLADUARTE"
    },
    "86865022": {
        "Centro Poblado": "LA ISLA"
    },
    "86885000": {
        "Centro Poblado": "VILLAGARZÓN"
    },
    "86885001": {
        "Centro Poblado": "PUERTO UMBRÍA"
    },
    "86885002": {
        "Centro Poblado": "LA CASTELLANA"
    },
    "86885004": {
        "Centro Poblado": "ALBANIA"
    },
    "86885007": {
        "Centro Poblado": "KOFANIA"
    },
    "86885008": {
        "Centro Poblado": "NARANJITO"
    },
    "86885009": {
        "Centro Poblado": "PORVENIR"
    },
    "86885011": {
        "Centro Poblado": "SANTA ROSA DE JUANAMBÚ"
    },
    "86885013": {
        "Centro Poblado": "CANANGUCHO"
    },
    "86885014": {
        "Centro Poblado": "RIO BLANCO"
    },
    "88001000": {
        "Centro Poblado": "SAN ANDRÉS,SAN ANDRÉS"
    },
    "88001001": {
        "Centro Poblado": "SAN ANDRÉS,LA LOMA"
    },
    "88001002": {
        "Centro Poblado": "SAN ANDRÉS,SAN LUIS"
    },
    "88001005": {
        "Centro Poblado": "SAN ANDRÉS,PUNTA SUR"
    },
    "88564000": {
        "Centro Poblado": "PROVIDENCIA,SANTA ISABEL"
    },
    "88564001": {
        "Centro Poblado": "PROVIDENCIA,FRESH WATER BAY"
    },
    "88564002": {
        "Centro Poblado": "PROVIDENCIA,SOUTH WEST BAY"
    },
    "88564003": {
        "Centro Poblado": "PROVIDENCIA,BOTTON HOUSE"
    },
    "88564004": {
        "Centro Poblado": "PROVIDENCIA,SAN FELIPE"
    },
    "88564005": {
        "Centro Poblado": "PROVIDENCIA,ROCKY POINT"
    },
    "88564006": {
        "Centro Poblado": "PROVIDENCIA,SANTA CATALINA"
    },
    "91001000": {
        "Centro Poblado": "LETICIA"
    },
    "91001001": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SANTA SOFÍA"
    },
    "91001002": {
        "Centro Poblado": "COMUNIDAD INDÍGENA NAZARETH"
    },
    "91001005": {
        "Centro Poblado": "COMUNIDAD INDÍGENA TIKUNA DE ARARA"
    },
    "91001007": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SAN MARTÍN DE AMACAYACÚ"
    },
    "91001009": {
        "Centro Poblado": "COMUNIDAD INDÍGENA ZARAGOZA"
    },
    "91001011": {
        "Centro Poblado": "COMUNIDAD INDÍGENA EL PROGRESO"
    },
    "91001012": {
        "Centro Poblado": "COMUNIDAD INDÍGENA EL VERGEL"
    },
    "91001013": {
        "Centro Poblado": "COMUNIDAD INDÍGENA PATIO DE CIENCIA DULCE  KM 11"
    },
    "91001014": {
        "Centro Poblado": "KILÓMETRO 6"
    },
    "91001015": {
        "Centro Poblado": "COMUNIDAD INDÍGENA LA LIBERTAD"
    },
    "91001016": {
        "Centro Poblado": "COMUNIDAD INDÍGENA LA MILAGROSA"
    },
    "91001017": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SECTOR LA PLAYA"
    },
    "91001018": {
        "Centro Poblado": "COMUNIDAD INDÍGENA MALOKA YAGUAS"
    },
    "91001019": {
        "Centro Poblado": "COMUNIDAD INDÍGENA LOMA LINDA"
    },
    "91001020": {
        "Centro Poblado": "COMUNIDAD INDÍGENA MACEDONIA"
    },
    "91001021": {
        "Centro Poblado": "COMUNIDAD INDÍGENA MOCAGUA"
    },
    "91001022": {
        "Centro Poblado": "COMUNIDAD INDÍGENA JUSSY MONILLA AMENA"
    },
    "91001023": {
        "Centro Poblado": "ASENTAMIENTO HUMANO TAKANA  KM 11"
    },
    "91001024": {
        "Centro Poblado": "COMUNIDAD INDÍGENA NUEVO JARDIN"
    },
    "91001025": {
        "Centro Poblado": "COMUNIDAD INDÍGENA PALMERAS"
    },
    "91001026": {
        "Centro Poblado": "COMUNIDAD INDÍGENA PUERTO TRIUNFO"
    },
    "91001027": {
        "Centro Poblado": "COMUNIDAD INDÍGENA ISLA DE RONDA"
    },
    "91001028": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SAN ANTONIO DE LOS LAGOS"
    },
    "91001029": {
        "Centro Poblado": "COMUNIDAD INDÍGENA ZIERA AMENA"
    },
    "91001030": {
        "Centro Poblado": "BARRIO SAN MIGUEL"
    },
    "91001031": {
        "Centro Poblado": "COMUNIDAD INDÍGENA CANAAN"
    },
    "91001032": {
        "Centro Poblado": "COMUNIDAD INDÍGENA PICHUNA KM 18"
    },
    "91001033": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SAN JOSÉ DEL RÍO"
    },
    "91001034": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SAN JUAN DE LOS PARENTES"
    },
    "91001035": {
        "Centro Poblado": "COMUNIDAD INDÍGENA SAN PEDRO DE LOS LAGOS"
    },
    "91263000": {
        "Centro Poblado": "EL ENCANTO"
    },
    "91405000": {
        "Centro Poblado": "LA CHORRERA"
    },
    "91407000": {
        "Centro Poblado": "LA PEDRERA"
    },
    "91430000": {
        "Centro Poblado": "PACOA"
    },
    "91460000": {
        "Centro Poblado": "MIRITÍ"
    },
    "91530000": {
        "Centro Poblado": "PUERTO ALEGRÍA"
    },
    "91536000": {
        "Centro Poblado": "PUERTO ARICA"
    },
    "91540000": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "91540001": {
        "Centro Poblado": "SAN JUAN DE ATACUARÍ"
    },
    "91540002": {
        "Centro Poblado": "BOYAHUAZÚ"
    },
    "91540003": {
        "Centro Poblado": "DOCE DE OCTUBRE"
    },
    "91540004": {
        "Centro Poblado": "NARANJALES"
    },
    "91540005": {
        "Centro Poblado": "PUERTO ESPERANZA"
    },
    "91540006": {
        "Centro Poblado": "PUERTO RICO"
    },
    "91540007": {
        "Centro Poblado": "SAN FRANCISCO"
    },
    "91540008": {
        "Centro Poblado": "SAN JUAN DEL SOCO"
    },
    "91540009": {
        "Centro Poblado": "SIETE DE AGOSTO"
    },
    "91540010": {
        "Centro Poblado": "SAN PEDRO DE TIPISCA"
    },
    "91540011": {
        "Centro Poblado": "VEINTE DE JULIO"
    },
    "91540012": {
        "Centro Poblado": "NUEVO PARAISO"
    },
    "91540013": {
        "Centro Poblado": "PATRULLEROS"
    },
    "91540014": {
        "Centro Poblado": "SAN JOSE DE VILLA ANDREA"
    },
    "91540015": {
        "Centro Poblado": "SANTA TERESITA"
    },
    "91540017": {
        "Centro Poblado": "VALENCIA"
    },
    "91669000": {
        "Centro Poblado": "PUERTO SANTANDER"
    },
    "91798000": {
        "Centro Poblado": "TARAPACÁ"
    },
    "94001000": {
        "Centro Poblado": "INÍRIDA"
    },
    "94001003": {
        "Centro Poblado": "COCO VIEJO"
    },
    "94001009": {
        "Centro Poblado": "RESGUARDO CACAHUAL RIO ATABAPO"
    },
    "94001010": {
        "Centro Poblado": "COCO NUEVO"
    },
    "94001011": {
        "Centro Poblado": "INSPECCION BARRANCO TIGRE"
    },
    "94001012": {
        "Centro Poblado": "COAYARE"
    },
    "94001013": {
        "Centro Poblado": "YURÍ"
    },
    "94001014": {
        "Centro Poblado": "SANTA ROSA"
    },
    "94001015": {
        "Centro Poblado": "SABANITAS"
    },
    "94343000": {
        "Centro Poblado": "BARRANCOMINAS"
    },
    "94343001": {
        "Centro Poblado": "MAPIRIPANA"
    },
    "94343002": {
        "Centro Poblado": "ARRECIFAL"
    },
    "94343005": {
        "Centro Poblado": "PUERTO ZANCUDO"
    },
    "94883000": {
        "Centro Poblado": "SAN FELIPE"
    },
    "94884000": {
        "Centro Poblado": "PUERTO COLOMBIA"
    },
    "94885000": {
        "Centro Poblado": "GALILEA"
    },
    "94886000": {
        "Centro Poblado": "CACAHUAL"
    },
    "94886003": {
        "Centro Poblado": "MEREY"
    },
    "94886004": {
        "Centro Poblado": "SAN JUAN"
    },
    "94887000": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "94887002": {
        "Centro Poblado": "VENADO ISANA"
    },
    "94888000": {
        "Centro Poblado": "MORICHAL - GARZA"
    },
    "95001000": {
        "Centro Poblado": "SAN JOSÉ DEL GUAVIARE"
    },
    "95001001": {
        "Centro Poblado": "RAUDAL DEL GUAYABERO"
    },
    "95001002": {
        "Centro Poblado": "SABANAS DE LA FUGA"
    },
    "95001006": {
        "Centro Poblado": "GUACAMAYAS"
    },
    "95001009": {
        "Centro Poblado": "PUERTO NUEVO"
    },
    "95001010": {
        "Centro Poblado": "PUERTO ARTURO"
    },
    "95001012": {
        "Centro Poblado": "CACHICAMO"
    },
    "95001016": {
        "Centro Poblado": "EL CAPRICHO"
    },
    "95001017": {
        "Centro Poblado": "CHARRAS"
    },
    "95001018": {
        "Centro Poblado": "CARACOL"
    },
    "95001019": {
        "Centro Poblado": "TOMACHIPÁN"
    },
    "95001020": {
        "Centro Poblado": "MOCUARE"
    },
    "95001023": {
        "Centro Poblado": "LA CARPA"
    },
    "95001024": {
        "Centro Poblado": "BOQUERÓN"
    },
    "95001027": {
        "Centro Poblado": "LAS ACACIAS"
    },
    "95001029": {
        "Centro Poblado": "RESBALÓN"
    },
    "95001030": {
        "Centro Poblado": "CAÑO BLANCO II"
    },
    "95001031": {
        "Centro Poblado": "CERRO AZUL"
    },
    "95001032": {
        "Centro Poblado": "EL DIAMANTE"
    },
    "95001034": {
        "Centro Poblado": "EL REFUGIO"
    },
    "95001035": {
        "Centro Poblado": "EL TRIUNFO"
    },
    "95001036": {
        "Centro Poblado": "LA ESMERALDA"
    },
    "95001037": {
        "Centro Poblado": "PICALOJO"
    },
    "95001039": {
        "Centro Poblado": "SANTO DOMINGO"
    },
    "95001042": {
        "Centro Poblado": "EL MORRO"
    },
    "95001043": {
        "Centro Poblado": "VILLA ALEJANDRA"
    },
    "95001044": {
        "Centro Poblado": "VILLA ALEJANDRA 2"
    },
    "95001045": {
        "Centro Poblado": "MIRALINDO"
    },
    "95001046": {
        "Centro Poblado": "LA CATALINA"
    },
    "95015000": {
        "Centro Poblado": "CALAMAR"
    },
    "95015003": {
        "Centro Poblado": "LAS DAMAS"
    },
    "95025000": {
        "Centro Poblado": "EL RETORNO"
    },
    "95025001": {
        "Centro Poblado": "LA LIBERTAD"
    },
    "95025002": {
        "Centro Poblado": "EL UNILLA"
    },
    "95025003": {
        "Centro Poblado": "CERRITOS"
    },
    "95025004": {
        "Centro Poblado": "MORICHAL VIEJO"
    },
    "95025005": {
        "Centro Poblado": "SAN LUCAS"
    },
    "95025006": {
        "Centro Poblado": "LA FORTALEZA"
    },
    "95025010": {
        "Centro Poblado": "LA PAZ"
    },
    "95025011": {
        "Centro Poblado": "PUEBLO NUEVO"
    },
    "95200000": {
        "Centro Poblado": "MIRAFLORES"
    },
    "95200001": {
        "Centro Poblado": "BARRANQUILLITA"
    },
    "95200002": {
        "Centro Poblado": "LAGOS DEL DORADO"
    },
    "95200003": {
        "Centro Poblado": "LAS PAVAS CAÑO TIGRE"
    },
    "95200004": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "95200005": {
        "Centro Poblado": "LA YE"
    },
    "95200006": {
        "Centro Poblado": "LAGOS DEL PASO"
    },
    "95200009": {
        "Centro Poblado": "PUERTO NARE"
    },
    "95200010": {
        "Centro Poblado": "PUERTO SANTANDER"
    },
    "95200014": {
        "Centro Poblado": "LA HACIENDA"
    },
    "95200015": {
        "Centro Poblado": "PUERTO CORDOBA"
    },
    "95200016": {
        "Centro Poblado": "PUERTO MANDU"
    },
    "97001000": {
        "Centro Poblado": "MITÚ"
    },
    "97001002": {
        "Centro Poblado": "CAMANAOS"
    },
    "97001005": {
        "Centro Poblado": "ACARICUARA"
    },
    "97001006": {
        "Centro Poblado": "VILLAFÁTIMA"
    },
    "97001008": {
        "Centro Poblado": "PIRAMIRÍ"
    },
    "97001009": {
        "Centro Poblado": "YAPÚ"
    },
    "97001010": {
        "Centro Poblado": "YURUPARÍ"
    },
    "97001011": {
        "Centro Poblado": "MARGEN IZQUIERDO"
    },
    "97001012": {
        "Centro Poblado": "12 DE OCTUBRE"
    },
    "97001013": {
        "Centro Poblado": "TAPURUCUARA"
    },
    "97161000": {
        "Centro Poblado": "CARURÚ"
    },
    "97511000": {
        "Centro Poblado": "PACOA"
    },
    "97511001": {
        "Centro Poblado": "ACAIPI"
    },
    "97666000": {
        "Centro Poblado": "TARAIRA"
    },
    "97777000": {
        "Centro Poblado": "PUERTO SOLANO (PAPUNAHUA)"
    },
    "97889000": {
        "Centro Poblado": "YAVARATÉ"
    },
    "99001000": {
        "Centro Poblado": "PUERTO CARREÑO"
    },
    "99001001": {
        "Centro Poblado": "LA VENTUROSA"
    },
    "99001002": {
        "Centro Poblado": "CASUARITO"
    },
    "99001003": {
        "Centro Poblado": "PUERTO MURILLO"
    },
    "99001004": {
        "Centro Poblado": "ACEITICO"
    },
    "99001005": {
        "Centro Poblado": "GARCITAS"
    },
    "99001006": {
        "Centro Poblado": "GUARIPA"
    },
    "99001007": {
        "Centro Poblado": "MORICHADA"
    },
    "99524000": {
        "Centro Poblado": "LA PRIMAVERA"
    },
    "99524001": {
        "Centro Poblado": "NUEVA ANTIOQUIA"
    },
    "99524002": {
        "Centro Poblado": "SANTA BÁRBARA"
    },
    "99524007": {
        "Centro Poblado": "SAN TEODORO (LA PASCUA)"
    },
    "99624000": {
        "Centro Poblado": "SANTA ROSALÍA"
    },
    "99624001": {
        "Centro Poblado": "GUACACÍAS"
    },
    "99773000": {
        "Centro Poblado": "CUMARIBO"
    },
    "99773001": {
        "Centro Poblado": "PALMARITO"
    },
    "99773002": {
        "Centro Poblado": "EL VIENTO"
    },
    "99773003": {
        "Centro Poblado": "TRES MATAS"
    },
    "99773004": {
        "Centro Poblado": "AMANAVÉN"
    },
    "99773005": {
        "Centro Poblado": "CHUPAVE"
    },
    "99773008": {
        "Centro Poblado": "GUANAPE"
    },
    "99773010": {
        "Centro Poblado": "PUERTO PRÍNCIPE"
    },
    "99773013": {
        "Centro Poblado": "PUERTO NARIÑO"
    },
    "99773015": {
        "Centro Poblado": "SANTA RITA"
    },
    "99773017": {
        "Centro Poblado": "CHAPARRAL"
    },
    "99773020": {
        "Centro Poblado": "EL PROGRESO"
    },
    "99773021": {
        "Centro Poblado": "EL TUPARRO"
    },
    "99773024": {
        "Centro Poblado": "BRISA"
    },
    "99773025": {
        "Centro Poblado": "GUATURIBA"
    },
    "99773026": {
        "Centro Poblado": "MATSULDANI"
    },
    "99773027": {
        "Centro Poblado": "REMANSO"
    },
    "50330003": {
        "Centro Poblado": "BRISAS DEL DUDA"
    },
    "50350016": {
        "Centro Poblado": "VILLA CARDONA"
    },
    "50350009": {
        "Centro Poblado": "ALTO MORROCOY (NUEVO HORIZONTE)"
    },
    "50350011": {
        "Centro Poblado": "LA TUNIA"
    },
    "50350002": {
        "Centro Poblado": "LOS POZOS"
    },
    "50711019": {
        "Centro Poblado": "BUENOS AIRES"
    },
    "81065003": {
        "Centro Poblado": "LOS ANGELITOS"
    },
    "27425016": {
        "Centro Poblado": "SAN FRANCISCO DE TAUCHIGADÓ"
    },
    "08549004": {
        "Centro Poblado": "PUNTA ASTILLEROS"
    },
    "08832014": {
        "Centro Poblado": "PUERTO CAIMÁN"
    },
    "13655002": {
        "Centro Poblado": "BERMÚDEZ"
    },
    "18756009": {
        "Centro Poblado": "PEÑA ROJA DEL CAGUAS"
    },
    "18756010": {
        "Centro Poblado": "LA MANÁ"
    },
    "20517007": {
        "Centro Poblado": "MATA DE BARRO"
    },
    "23162031": {
        "Centro Poblado": "CONDOMINIO LAGOS DE SANTA RITA"
    },
    "23555029": {
        "Centro Poblado": "SAN JERÓNIMO (GOLERO)"
    },
    "23675017": {
        "Centro Poblado": "BARCELONA"
    },
    "47570008": {
        "Centro Poblado": "ISLA DE CATAQUITA"
    },
    "63594008": {
        "Centro Poblado": "TROCADEROS"
    },
    "70429030": {
        "Centro Poblado": "TOTUMAL"
    },
    "70678006": {
        "Centro Poblado": "LOS ÁNGELES"
    },
    "76109066": {
        "Centro Poblado": "LA DELFINA"
    },
    "76109126": {
        "Centro Poblado": "PLAYA LARGA"
    },
    "85010011": {
        "Centro Poblado": "TURUA"
    },
    "97001003": {
        "Centro Poblado": "MACUANA"
    },
    "23300002": {
        "Centro Poblado": "LOS GÓMEZ"
    },
    "44378001": {
        "Centro Poblado": "TABACO"
    },
    "44378002": {
        "Centro Poblado": "CERRO ALTO"
    },
    "44378006": {
        "Centro Poblado": "GUAMACHITO"
    },
    "44378008": {
        "Centro Poblado": "LA GLORIA"
    },
    "44378011": {
        "Centro Poblado": "MANANTIAL GRANDE"
    },
    "44378012": {
        "Centro Poblado": "YAGUARITO"
    },
    "70702002": {
        "Centro Poblado": "HATO VIEJO"
    },
    "27086": {
        "Municipio": "BELEN DE BAJIRA"
    },
    "70001010": {
        "Centro Poblado": "Palmito - Las Huertas"
    },
    "44090009": {
        "Centro Poblado": "RIO NEGRO"
    },
    "23678017": {
        "Centro Poblado": "CAROLINA"
    },
    "84530000": {
        "Centro Poblado": "TRINIDAD"
    },
    "44857000": {
        "Centro Poblado": "URIBIA"
    },
    "18785006": {
        "Centro Poblado": "KILOMETRO 36"
    },
    "23807034": {
        "Centro Poblado": "BONITO VIENTO"
    },
    "95001041": {
        "Centro Poblado": "TIENDA NUEVA"
    },
    "85430002": {
        "Centro Poblado": "GUAMAL"
    },
    "25181001": {
        "Centro Poblado": "ALTO DEL PALO"
    },
    "25040005": {
        "Centro Poblado": "BOQUERÓN DE ILO"
    },
    "25793002": {
        "Centro Poblado": "ROMA"
    },
    "25815008": {
        "Centro Poblado": "SAN CARLOS"
    },
    "27493": {
        "Municipio": "NUEVO BELÉN DE BAJIRÁ"
    },
    "50711001": {
        "Centro Poblado": "CAMPO ALEGRE"
    },
    "18753030": {
        "Centro Poblado": "LA CHORRERA"
    },
    "76109101": {
        "Centro Poblado": "LAS PALMAS"
    }
}

# =============================================
# FUNCIONES AUXILIARES
# =============================================

def setup_namespaces():
    """Registra los namespaces globalmente para ET"""
    for prefix, uri in NSMAP.items():
        if prefix:
            ET.register_namespace(prefix, uri)
        else:
            ET.register_namespace('', uri)

def create_element(parent, tag, text=None, attributes=None):
    """Crea un elemento XML con namespace"""
    try:
        if ':' in tag:
            namespace, tag_name = tag.split(':')
            ns_uri = NSMAP[namespace] if namespace else NSMAP[None]
            element = ET.SubElement(parent, f'{{{ns_uri}}}{tag_name}')
        else:
            ns_uri = NSMAP[None]
            element = ET.SubElement(parent, f'{{{ns_uri}}}{tag}')
        
        if text is not None:
            element.text = str(text)
        if attributes:
            for key, value in attributes.items():
                element.set(key, value)
        
        return element
    except Exception as e:
        arcpy.AddWarning(f"Error creating XML element {tag}: {str(e)}")
        raise

def validate_inputs(raster_path, boundary_fc, output_folder):
    """Valida los parámetros de entrada"""
    errors = []
    
    if not raster_path.lower().endswith('.tif'):
        errors.append("El archivo de entrada debe ser un TIF")
    
    if not arcpy.Exists(raster_path):
        errors.append(f"El raster {raster_path} no existe")
    
    if not arcpy.Exists(boundary_fc):
        errors.append(f"La capa de límites {boundary_fc} no existe")
    
    if not os.path.exists(output_folder):
        errors.append(f"La carpeta de salida {output_folder} no existe")
    
    if errors:
        for error in errors:
            arcpy.AddError(error)
            arcpy.AddWarning(error)
        return False
    
    return True

def format_proper_name(text):
    """
    Formatea correctamente nombres propios:
    - Si el nombre está en dane_dict_departamentos, aplica formato de departamento (artículo en minúscula).
    - Si no, aplica formato de nombre estándar (como centros poblados o municipios).
    
    Nota: Usa la variable global dane_dict
    """
    
    # Lista de palabras a mantener en minúsculas (excepto si son la primera palabra)
    lowercase_words = ['de', 'del', 'la', 'las', 'los', 'y', 'e', 'o', 'u']
    
    # Usar la variable global dane_dict
    global dane_dict
    
    # Crear set de nombres de departamentos (solo elementos que tengan la clave "Departamento")
    nombres_departamentos = set()
    if 'dane_dict' in globals():
        nombres_departamentos = {
            v["Departamento"].strip().upper() 
            for v in dane_dict.values() 
            if "Departamento" in v
        }
    
    # Limpiar y convertir a mayúsculas para comparación
    clean_text = text.strip().upper()
    
    if clean_text in nombres_departamentos:
        # Es un nombre de departamento con DE/DEL → aplicar lógica especial
        words = clean_text.lower().split()
        formatted = [
            word if word in lowercase_words else word.capitalize()
            for word in words
        ]
        return ' '.join(formatted)
    else:
        # Es un nombre común (municipio, centro poblado, etc.) → aplicar lógica estándar
        result = text.title().strip()
        words = result.split()
        for i in range(1, len(words)):
            if words[i].lower() in lowercase_words:
                words[i] = words[i].lower()
        return ' '.join(words)
    

def parse_filename(filename, dane_dict):
    """Extrae GSD, códigos y nombres desde el nombre del archivo usando dane_dict
        determina tipo de producto y centro poblado si e cabecera o no
    """
    try:
        # Ejemplo: MDT1_66045000_20200621.tif
        filename = filename.replace('.tif', '')  # quitar extensión si está
        parts = filename.split('_')
        
        if len(parts) < 3:
            raise ValueError("Formato de nombre de archivo incorrecto")
        
        gsd = parts[0].replace('MDT', '')  # 10
        code = parts[1]  # 66045000
        date_str = parts[2]  # 20200621

        # Desglosar el código
        dept_code = code[:2]       # Ej: 66
        mpio_code = code[:5]       # Ej: 66045
        cpob_code = code           # Ej: 66045000

        # Buscar nombres en dane_dict
        departamento = dane_dict.get(dept_code, {}).get("Departamento", "Desconocido")
        municipio = dane_dict.get(mpio_code, {}).get("Municipio", "Desconocido")
        centro_poblado = dane_dict.get(cpob_code, {}).get("Centro Poblado", "Desconocido")

        # Normalizar nombres
        departamento = format_proper_name(departamento.title())
        municipio = format_proper_name(municipio.title())
        centro_poblado = format_proper_name(centro_poblado.title())

        # Determinar el tipo de centro poblado
        if cpob_code.endswith("000"):
            tipo_centro = "Cabecera Municipal"
        else:
            if  centro_poblado == "Desconocido":
                tipo_centro = "Desconocido"
            else:
                tipo_centro = "Centro Poblado"

        return {
            'gsd': gsd,
            'departamento': departamento,
            'municipio': municipio,
            'centro_poblado': centro_poblado,
            'tipo_centro': tipo_centro,
            'fecha': datetime.strptime(date_str, '%Y%m%d')
        }

    except Exception as e:
        arcpy.AddWarning(f"Error parsing filename {filename}: {str(e)}")
        raise


def get_spatial_info(boundary_fc, raster_path):
    """Obtiene información espacial de la capa de límites"""
    try:
        # Definir SR WGS84
        sr_wgs84 = arcpy.SpatialReference(4326)  # WGS84
        sr_9377 = arcpy.SpatialReference(9377)  # Origen Nacional
        with arcpy.da.SearchCursor(boundary_fc, ["SHAPE@AREA", "SHAPE@"]) as cursor:
            for row in cursor:
                area_ha = row[0] / 10000.0  # Convertir de m² a hectáreas
                #obtener el extent del primer feature en coordenadas geográficas
                # Reproyectar a WGS84
                geom_wgs84 = row[1].projectAs(sr_wgs84)
                extent = geom_wgs84.extent
        extent2 = arcpy.Describe(raster_path).extent
        extent2 = extent2.projectAs(sr_9377)  # Reproyectar a Origen Nacional 
        return area_ha, extent, extent2
    except Exception as e:
        arcpy.AddWarning(f"Error obteniendo información espacial: {str(e)}")
        raise

#Diccionario para manejar las escalas aplicables dependiendo del GSD
GSD_TO_ESCALA = {
    1: "1:1.000",
    2: "1:2.000",
    5: "1:5.000",
    10: "1:10.000",
    25: "1:25.000",
    50: "1:50.000",
    100: "1:100.000"
}

def get_escala_por_gsd(gsd_cm):
    gsd_cm = float(gsd_cm)
    for umbral in sorted(GSD_TO_ESCALA):
        if gsd_cm <= umbral:
            return GSD_TO_ESCALA[umbral]
    return "desconocida"

def normalizar(texto):
    """Normaliza texto eliminando tildes, espacios extras y pasando a minúsculas."""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().lower()


def create_root_metadata():
    """Crea el elemento raíz con todos los namespaces necesarios"""
    # Registrar los namespaces primero
    ET.register_namespace('', NSMAP[None])  # Default namespace
    for prefix, uri in NSMAP.items():
        if prefix:  # Skip None
            ET.register_namespace(prefix, uri)
    
    # Crear el elemento raíz
    root = ET.Element('{' + NSMAP[None] + '}MD_Metadata')
    
    # No necesitamos agregar los namespaces como atributos ya que
    # ElementTree los agregará automáticamente al guardar
    
    # Agregar schema location
    xsi_ns = NSMAP['xsi']
    root.set(f'{{{xsi_ns}}}schemaLocation', 
             'http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd')
    
    return root


def generar_thumbnail(input_layer_path, output_folder, usar_layout_existente="false"):
    """
    Genera un thumbnail (PNG) de una capa de entrada (shapefile o raster) en ArcGIS Pro.
    Puede crear un mapa temporal o usar el primer layout existente del proyecto.

    Parámetros:
    0 - Capa de entrada (feature class o raster dataset)
    1 - Carpeta de salida del PNG
    2 - Usar layout existente ("true" o "false"). Si es "true", usa el primer layout del proyecto
    """
    try:
        if not arcpy.Exists(input_layer_path):
            arcpy.AddError(f"La capa de entrada no existe: {input_layer_path}")
            raise arcpy.ExecuteError

        if not os.path.exists(output_folder):
            arcpy.AddError(f"La carpeta de salida no existe: {output_folder}")
            raise arcpy.ExecuteError

        nombre_base = os.path.splitext(os.path.basename(input_layer_path))[0]
        output_png_path = os.path.join(output_folder, f"{nombre_base}_thumbnail.png")

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        
        # Si usar_layout_existente es "true", usar el primer layout del proyecto
        if usar_layout_existente.lower() == "true":
            layouts = aprx.listLayouts()
            if not layouts:
                arcpy.AddError("No se encontraron layouts en el proyecto actual")
                raise arcpy.ExecuteError
            
            layout = layouts[0]  # Tomar el primer layout
            arcpy.AddMessage(f"Usando layout existente: {layout.name}")
            
            # Exportar directamente el layout existente
            layout.exportToPNG(output_png_path, 200)
            
            # Crear copia
            
            return output_png_path
        
        # Comportamiento original: crear mapa y layout temporal
        else:
            temp_map_name = f"Mapa_Temporal_{nombre_base}"
            new_map = aprx.createMap(temp_map_name)

            # Eliminar basemaps si existen
            basemap_layers = [lyr for lyr in new_map.listLayers() if lyr.isBasemapLayer]
            for basemap_layer in basemap_layers:
                new_map.removeLayer(basemap_layer)

            # Agregar capa al mapa
            layer = new_map.addDataFromPath(input_layer_path)

            layout_name = f"ThumbnailLayout_{nombre_base}"
            layout = aprx.createLayout(10, 6, 'INCH', layout_name)

            mf = layout.createMapFrame(arcpy.Point(-0.1, -0.1), new_map, 'Punto')
            mf.elementWidth = 10.2
            mf.elementHeight = 6.2

            # Ajustar extensión a la capa
            try:
                mf.camera.setExtent(mf.getLayerExtent(layer))
                mf.camera.scale *= 1.1
            except Exception as e:
                arcpy.AddWarning(f"No se pudo ajustar la extensión: {str(e)}")

            layout.exportToPNG(output_png_path, 200)

            aprx.deleteItem(layout)
            aprx.deleteItem(new_map)
            aprx.save()

            return output_png_path

    except Exception as e:
        arcpy.AddError(f"Error al generar thumbnail: {str(e)}")
        raise

def save_metadata(root, output_folder, identifier):
    """Guarda los metadatos en un archivo XML con formato usando solo la biblioteca estándar"""
    try:

        output_xml = os.path.join(output_folder, f"{identifier}.xml")
        
        # Crear un string XML crudo primero
        xml_str = ET.tostring(root, encoding='utf-8')
        
        # Usar xml.dom.minidom de manera segura para formatear
        from xml.dom import minidom
        
        # Crear un objeto DOM desde el XML, pero preservando las declaraciones de namespace
        dom = minidom.parseString(xml_str)
        
        # Escribir con formato bonito pero con cuidado al manejar los namespaces
        with open(output_xml, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            
            # Usar la función toprettyxml pero omitiendo la declaración XML
            pretty_xml = dom.documentElement.toprettyxml(indent="  ")
            f.write(pretty_xml)
        
        arcpy.AddMessage(f"✅ Metadatos creados exitosamente")

        return output_xml
        
    except Exception as e:
        arcpy.AddWarning(f"Error guardando archivo de metadatos: {str(e)}")
        raise

def importar_y_exportar_metadatos(ruta_raster, ruta_xml_entrada, ruta_xml_salida, ruta_thumbnail):
    """
    Importa metadatos en formato estándar (ISO19139, FGDC, etc.) a un ráster y luego los exporta nuevamente.

    Parámetros:
        ruta_raster (str): Ruta del ráster al que se le asignarán los metadatos.
        ruta_xml_entrada (str): Ruta al archivo XML de entrada (formato estándar).
        ruta_xml_salida (str): Ruta al archivo XML donde se exportarán los metadatos.
        formato_entrada (str): Formato del XML de entrada. Ej: 'ISO19139', 'FGDC_CSDGM'
    """
    try:
        # Obtener objeto de metadatos del ráster
        md_raster = md.Metadata(ruta_raster)

        if md_raster.isReadOnly:
            arcpy.AddWarning("❌ El objeto de metadatos es de solo lectura. No se puede modificar.")
            return
        
        # Borrar el metadato del raster (ruta_raster.xml)
        try:
            ruta_xml = ruta_raster + ".xml"
            if os.path.exists(ruta_xml):
                os.remove(ruta_xml)
                #arcpy.AddMessage("Removiendo metadatos previos")
        except Exception as e:
            arcpy.AddMessage(f"⚠️ No se pudo borrar metadato: {e}")
        # Asignar thumbnail
        md_raster.thumbnailUri = ruta_thumbnail
        arcpy.AddMessage("✅ Thumbnail cargado exitosamente.")

        #Importar Metadato
        md_raster.importMetadata(ruta_xml_entrada)
        md_raster.save()
        md_raster.synchronize('ACCESSED')

        #Borrar el historial de geoprocesamiento del metadato
        md_raster.deleteContent('GPHISTORY')
        #arcpy.AddMessage("✅ Historial de geoprocesamiento eliminado.")


        # Guardar todos los cambios
        md_raster.save()
        arcpy.AddMessage("✅ Metadatos importados correctamente.")

        #Exportar el metadato
        md_raster.exportMetadata(ruta_xml_salida, 'ISO19139_GML32')
        #arcpy.AddMessage("✅ Exportación finalizada.")

        try:
            os.remove(ruta_thumbnail)
        except:
            pass


    except Exception as e:
        arcpy.AddError(f"Error en el proceso: {e}")


# ===============================================================
# FUNCIONES PARA GENERACIÓN DE METADATOS DE MODELOS DE TERRENO
# ===============================================================

def MDT_add_basic_metadata_sections(root, filename, location_data):
    """Agrega secciones básicas de metadatos"""
    try:
        #Fileidentifier etiqueta
        # Ejemplo: MDT1_66045000_20200621.tif, resultado MDT10_Metadato_66045000_20200621.tif
        filename = filename.replace('.tif', '')  # quitar extensión si está
        parts = filename.split('_')
        
        if len(parts) < 3:
            raise ValueError("Formato de nombre de archivo incorrecto")
        
        gsd = location_data['gsd_nombre']

        # Extraer partes del nombre
        code = parts[1]
        date_str = parts[2]

        # Construir el identificador
        identifier = f'MDT{gsd}_Metadato_{code}_{date_str}'

        arcpy.AddMessage(f"Identificador: {identifier}")

        id_element = create_element(root, 'fileIdentifier')
        create_element(id_element, 'gco:CharacterString', identifier) 

        
        # Language
        lang = create_element(root, 'language')
        code = create_element(lang, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')
        
        # Character Set
        char_set = create_element(root, 'characterSet')
        code = create_element(char_set, 'MD_CharacterSetCode', 'utf8')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        code.set('codeListValue', 'utf8')
        code.set('codeSpace', 'ISOTC211/19115')
        
        # Hierarchy Level
        hierarchy = create_element(root, 'hierarchyLevel')
        code = create_element(hierarchy, 'MD_ScopeCode', 'dataset')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
        code.set('codeListValue', 'dataset')
        code.set('codeSpace', 'ISOTC211/19115')
        
        # Hierarchy Level Name
        hierarchy_name = create_element(root, 'hierarchyLevelName')
        create_element(hierarchy_name, 'gco:CharacterString', 'dataset')
        
        # Date Stamp (Fecha de ultima actualización no automatica)
        # Fecha de publicación = 15 días después de la fecha de creación
        publication_datetime = datetime.now() + timedelta(days=15)
        publication_date_str = publication_datetime.strftime("%Y-%m-%d")
        create_element(create_element(root, 'dateStamp'), 'gco:Date', publication_date_str)

        # Metadata Standard
        create_element(create_element(root, 'metadataStandardName'), 'gco:CharacterString', 
                      'ISO 19139 Geographic Information - Metadata - Implementation Specification')
        create_element(create_element(root, 'metadataStandardVersion'), 'gco:CharacterString', '2007')
        
        # Locale
        locale = create_element(root, 'locale')
        pt_locale = create_element(locale, 'PT_Locale')
        
        lang_code = create_element(pt_locale, 'languageCode')
        code = create_element(lang_code, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')
        
        country = create_element(pt_locale, 'country')
        country_code = create_element(country, 'Country', 'CO')
        country_code.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_code.set('codeListValue', 'CO')
        country_code.set('codeSpace', 'ISO3166-1')
        
        char_enc = create_element(pt_locale, 'characterEncoding')
        enc_code = create_element(char_enc, 'MD_CharacterSetCode', 'utf8')
        enc_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        enc_code.set('codeListValue', 'utf8')
        enc_code.set('codeSpace', 'ISOTC211/19115')
                
        arcpy.AddMessage("Secciones básicas de metadatos agregadas correctamente")
        return identifier
    except Exception as e:
        arcpy.AddWarning(f"Error agregando secciones básicas: {str(e)}")
        raise

def MDT_add_contact_info(root, EXTERNO):
    """Agrega información de contacto"""
    try:
        contact = create_element(root, 'contact')
        party = create_element(contact, 'CI_ResponsibleParty')
        
        # Agregar individualName antes de organisationName (orden es importante)
        #individual = create_element(party, 'individualName')
        #create_element(individual, 'gco:CharacterString', ORGANIZATION_INFO['name'])
        
        # El resto del código se mantiene igual...
        create_element(create_element(party, 'organisationName'), 'gco:CharacterString', EXTERNO['name'])
        create_element(create_element(party, 'positionName'), 'gco:CharacterString', EXTERNO['position'])
        
        # Información de contacto
        contact_info = create_element(party, 'contactInfo')
        ci_contact = create_element(contact_info, 'CI_Contact')
        
        # Teléfono
        phone = create_element(ci_contact, 'phone')
        tel = create_element(phone, 'CI_Telephone')
        voice = create_element(tel, 'voice')
        create_element(voice, 'gco:CharacterString', EXTERNO['phone'])
        
        # Dirección
        address = create_element(ci_contact, 'address')
        addr = create_element(address, 'CI_Address')
        
        delivery = create_element(addr, 'deliveryPoint')
        create_element(delivery, 'gco:CharacterString', EXTERNO['address'])
        
        city = create_element(addr, 'city')
        create_element(city, 'gco:CharacterString', EXTERNO['city'])
        
        area = create_element(addr, 'administrativeArea')
        create_element(area, 'gco:CharacterString', EXTERNO['state'])
        
        postal = create_element(addr, 'postalCode')
        create_element(postal, 'gco:CharacterString', EXTERNO['postal'])
        
        country = create_element(addr, 'country')
        country_code = create_element(country, 'Country', EXTERNO['country'])
        country_code.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_code.set('codeListValue', EXTERNO['country'])
        country_code.set('codeSpace', 'ISO3166-1')
        
        email = create_element(addr, 'electronicMailAddress')
        create_element(email, 'gco:CharacterString', EXTERNO['email'])
        
        # Rol
        role = create_element(party, 'role')
        code = create_element(role, 'CI_RoleCode', EXTERNO['role'])
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
        code.set('codeListValue', EXTERNO['role'])
        code.set('codeSpace', 'ISOTC211/19115')
        
        arcpy.AddMessage("Información de contacto agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de contacto: {str(e)}")
        raise

def MDT_add_identification_info(root, identifier, location_data, extent, area_ha, sensor, puntos_lidar, ORGANIZATION_INFO):
    """Agrega información de identificación del recurso"""
    try:
        ident = create_element(root, 'identificationInfo')
        data_ident = create_element(ident, 'MD_DataIdentification')
        
        # Citation
        citation = create_element(data_ident, 'citation')
        ci_citation = create_element(citation, 'CI_Citation')
        
        # Título
        title = create_element(ci_citation, 'title')

        # Determinar título dinámico según jerarquía disponible
        # Construcción del título
        if location_data['tipo_centro'] == "Cabecera Municipal":
            nombre_municipio = location_data['municipio']
            nombre_cabecera = location_data['centro_poblado']

            # Comparación normalizada para detectar si hay redundancia
            if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                title_text = (
                    f"Modelo Digital de Terreno. Departamento {location_data['departamento']}. "
                    f"Cabecera Municipal de {nombre_cabecera}. "
                    f"Malla {location_data['gsd']} m. "
                    f"Año {location_data['fecha'].year}"
                )
            else:
                title_text = (
                    f"Modelo Digital de Terreno. Departamento {location_data['departamento']}. "
                    f"Municipio de {nombre_municipio}. "
                    f"Cabecera Municipal de {nombre_cabecera}. "
                    f"Malla {location_data['gsd']} m. "
                    f"Año {location_data['fecha'].year}"
                )
        elif location_data['centro_poblado'] != "Desconocido":
            title_text = (
                f"Modelo Digital de Terreno. Departamento {location_data['departamento']}. "
                f"Municipio de {location_data['municipio']}. "
                f"{location_data['tipo_centro']} de {location_data['centro_poblado']}. "
                f"Malla {location_data['gsd']} m. "
                f"Año {location_data['fecha'].year}"
            )
        elif location_data['municipio'] != "Desconocido":
            title_text = (
                f"Modelo Digital de Terreno. Departamento {location_data['departamento']}. "
                f"Municipio de {location_data['municipio']}. "
                f"Malla {location_data['gsd']} m. "
                f"Año {location_data['fecha'].year}"
            )
        else:
            title_text = (
                f"Modelo Digital de Terreno. Departamento {location_data['departamento']}. "
                f"Malla {location_data['gsd']} m. "
                f"Año {location_data['fecha'].year}"
            )


        create_element(title, 'gco:CharacterString', title_text)

        # Titulo alternativo
        alt_title = create_element(ci_citation, 'alternateTitle')
        
        alternative_titulo = identifier.split('_')
        
        # Extraer partes del nombre
        code = alternative_titulo[2]
        date_str = alternative_titulo[3]
        gsd = alternative_titulo[0]

        # Construir el identificador
        identifieralt = f'{gsd}_{code}_{date_str}'

        create_element(alt_title, 'gco:CharacterString', identifieralt)

        
        # Fechas de creacion  y publicacion
        # Generar hora aleatoria para fecha de creación (horario laboral)
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        # Fecha de creación con hora aleatoria
        creation_datetime = datetime(
            location_data['fecha'].year,
            location_data['fecha'].month,
            location_data['fecha'].day,
            hour,
            minute,
            second
        )
        creation_date_str = creation_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        # Fecha de publicación = 15 días después de la fecha de creación
        publication_datetime = datetime.now() + timedelta(days=15)
        publication_date_str = publication_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        # === Fecha de creación ===
        date = create_element(ci_citation, 'date')
        ci_date = create_element(date, 'CI_Date')

        create_element(create_element(ci_date, 'date'), 'gco:DateTime', creation_date_str)

        date_type = create_element(ci_date, 'dateType')
        code = create_element(date_type, 'CI_DateTypeCode', 'creation')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode')
        code.set('codeListValue', 'creation')
        code.set('codeSpace', 'ISOTC211/19115')

        # === Fecha de publicación ===
        date = create_element(ci_citation, 'date')
        pu_date = create_element(date, 'CI_Date')

        create_element(create_element(pu_date, 'date'), 'gco:DateTime', publication_date_str)

        pu_date_type = create_element(pu_date, 'dateType')
        pu_code = create_element(pu_date_type, 'CI_DateTypeCode', 'publication')
        pu_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode')
        pu_code.set('codeListValue', 'publication')
        pu_code.set('codeSpace', 'ISOTC211/19115')

        # Dentro de ci_citation, presentation formats
        presentation_form = create_element(ci_citation, 'presentationForm')
        create_element(
            presentation_form,
            'CI_PresentationFormCode',
            text='modelDigital',
            attributes={
                'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_PresentationFormCode',
                'codeListValue': 'modelDigital',
                'codeSpace': 'ISOTC211/19115'
            }
        )

        #CREAR CONTACTO EN CITATION

        def crear_contacto_citation(ci_citation, diccionario):
            cited_party = create_element(ci_citation, 'citedResponsibleParty')
            responsible_party = create_element(cited_party, 'CI_ResponsibleParty')
            #create_element(create_element(responsible_party, 'individualName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
            create_element(create_element(responsible_party, 'organisationName'), 'gco:CharacterString', diccionario['name'])
            create_element(create_element(responsible_party, 'positionName'), 'gco:CharacterString', diccionario['position'])

            # Contact info
            contact_info = create_element(responsible_party, 'contactInfo')
            ci_contact = create_element(contact_info, 'CI_Contact')

            # Teléfono
            phone = create_element(ci_contact, 'phone')
            ci_phone = create_element(phone, 'CI_Telephone')
            create_element(create_element(ci_phone, 'voice'), 'gco:CharacterString', diccionario['phone'])

            # Dirección
            address = create_element(ci_contact, 'address')
            ci_address = create_element(address, 'CI_Address')

            create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString', diccionario['address'])
            create_element(create_element(ci_address, 'city'), 'gco:CharacterString', diccionario['city'])
            if diccionario.get('state'):
                create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', diccionario['state'])
            create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', diccionario['postal'])

            country = create_element(ci_address, 'country')
            country_el = create_element(country, 'Country', diccionario['country'])
            country_el.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
            country_el.set('codeListValue', diccionario['country'])
            country_el.set('codeSpace', 'ISO3166-1')

            create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString', diccionario['email'])

            # Horario
            create_element(create_element(ci_contact, 'hoursOfService'), 'gco:CharacterString', diccionario['hours'])
            create_element(create_element(ci_contact, 'contactInstructions'), 'gco:CharacterString',diccionario['instructions'])
            
            #Rol
            role = create_element(responsible_party, 'role')
            role_code = create_element(role, 'CI_RoleCode', diccionario['role'])
            role_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
            role_code.set('codeListValue', diccionario['role'])
            role_code.set('codeSpace', 'ISOTC211/19115')
        
        #Crear contacto  Rol originador
        crear_contacto_citation(ci_citation, ORGANIZATION_INFO )
        
        # Abstract ------------------------------------------------------------
        if puntos_lidar == "true":
            puntos_lidar = f"puntos LIDAR provenientes del sensor"
        else:
            puntos_lidar = f"imágenes provenientes del sensor"



        def generar_abstract(location_data, area_ha, sensor, puntos_lidar):
            gsd = location_data["gsd"]
            escala = get_escala_por_gsd(gsd) 
            fecha_formateada = location_data["fecha"].strftime("%d de %B de %Y")
            if gsd == "1":
                unidad = "metro"
            else:
                unidad = "metros"
            partes_ubicacion = []

            if location_data.get("tipo_centro") == "Cabecera Municipal":
                nombre_municipio = location_data.get("municipio", "")
                nombre_cabecera = location_data.get("centro_poblado", "")

                if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                else:
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                    partes_ubicacion.append(f"municipio de {nombre_municipio}")

                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            
            elif location_data.get("tipo_centro") == "Centro Poblado":
                if location_data.get("centro_poblado") and location_data.get("centro_poblado") != "Desconocido":
                    partes_ubicacion.append(f"del centro poblado {location_data.get('centro_poblado')}")
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"municipio de {location_data.get('municipio')}")
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            elif location_data.get("municipio") == "Desconocido":
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"del departamento {location_data.get('departamento')}")

            elif location_data.get("centro_poblado") == "Desconocido":
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"del municipio de {location_data.get('municipio')}")
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            

            ubicacion = ", ".join(partes_ubicacion)

            abstract_text = (
                f"El modelo digital del terreno corresponde a una malla regular de puntos o celdas ráster espaciadas cada {gsd} {unidad}, " 
                f"aplicable para cartografía a escala {escala}. "
                f"Este producto contiene información {ubicacion}, República de Colombia. "
                f"Tiene una extensión de {area_ha:,.2f} hectáreas. "
                f"El proceso se realizó con {puntos_lidar} {sensor} del día {fecha_formateada}."
            )

            return abstract_text, escala


        abstract_text, escala = generar_abstract(location_data, area_ha, sensor, puntos_lidar)         
        create_element(create_element(data_ident, 'abstract'), 'gco:CharacterString', abstract_text)
        
        # Purpose
        purpose_text = ("Servir como insumo básico para la realización de estudios suburbanos y rurales como análisis de riesgos y amenazas, "
        "análisis hidrológicos, planificación de ordenación y manejo ambiental, ordenamiento territorial, deslindes, análisis espacial, entre otros.")
        create_element(create_element(data_ident, 'purpose'), 'gco:CharacterString', purpose_text)
        
        # Status
        status = create_element(data_ident, 'status')
        code = create_element(status, 'MD_ProgressCode', 'completed')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ProgressCode')
        code.set('codeListValue', 'completed')
        code.set('codeSpace', 'ISOTC211/19115')

        # Point of Contact
        poc = create_element(data_ident, 'pointOfContact')
        party = create_element(poc, 'CI_ResponsibleParty')

        #create_element(create_element(party, 'individualName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
        create_element(create_element(party, 'organisationName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
        create_element(create_element(party, 'positionName'), 'gco:CharacterString', ORGANIZATION_INFO['position'])

        # Contact Info
        contact_info = create_element(party, 'contactInfo')
        contact = create_element(contact_info, 'CI_Contact')

        # Teléfono
        phone = create_element(contact, 'phone')
        telephone = create_element(phone, 'CI_Telephone')
        create_element(create_element(telephone, 'voice'), 'gco:CharacterString', ORGANIZATION_INFO['phone'])

        # Dirección
        address = create_element(contact, 'address')
        ci_address = create_element(address, 'CI_Address')

        create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString', ORGANIZATION_INFO['address'])
        create_element(create_element(ci_address, 'city'), 'gco:CharacterString', ORGANIZATION_INFO['city'])
        create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', ORGANIZATION_INFO['state'])
        create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', ORGANIZATION_INFO['postal'])

        country = create_element(ci_address, 'country')
        country_el = create_element(country, 'Country', ORGANIZATION_INFO['country'])
        country_el.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_el.set('codeListValue', ORGANIZATION_INFO['country'])
        country_el.set('codeSpace', 'ISO3166-1')

        create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString', ORGANIZATION_INFO['email'])

        # Horario de atención
        create_element(create_element(contact, 'hoursOfService'), 'gco:CharacterString', ORGANIZATION_INFO['hours'])
        create_element(create_element(contact, 'contactInstructions'), 'gco:CharacterString',
                    ORGANIZATION_INFO['instructions'])

        # Rol
        role = create_element(party, 'role')
        role_code = create_element(role, 'CI_RoleCode', 'resourceProvider')
        role_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
        role_code.set('codeListValue', 'resourceProvider')
        role_code.set('codeSpace', 'ISOTC211/19115')
        
        
        # Language
        lang = create_element(data_ident, 'language')
        code = create_element(lang, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')

        # Mantenimieto
        resource_maintenance = create_element(data_ident, 'resourceMaintenance')
        md_maintenance = create_element(resource_maintenance, 'MD_MaintenanceInformation')
        update_freq = create_element(md_maintenance, 'maintenanceAndUpdateFrequency')

        create_element(update_freq, 'MD_MaintenanceFrequencyCode', text='asNeeded', attributes={
            'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode',
            'codeListValue': 'asNeeded',
            'codeSpace': 'ISOTC211/19115'
        })

        
        # NUEVA SECCIÓN: Keywords geográficas con codeListValue="place"
        place_kw_section = create_element(data_ident, 'descriptiveKeywords')
        place_keywords = create_element(place_kw_section, 'MD_Keywords')

        nombre_departamento = location_data.get("departamento", "")
        nombre_municipio = location_data.get("municipio", "")
        nombre_cabecera = location_data.get("centro_poblado", "")
        tipo_centro = location_data.get("tipo_centro", "")

        if nombre_municipio == "Desconocido":
            dynamic_keywords = f"República de Colombia, Departamento {nombre_departamento}"
        else:
            if nombre_cabecera == "Desconocido":
                dynamic_keywords = f"República de Colombia, Departamento {nombre_departamento}, Municipio de {nombre_municipio}"
            else:
                if tipo_centro == "Cabecera Municipal":
                    if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                        dynamic_keywords = (
                            f"República de Colombia, Departamento {nombre_departamento}, "
                            f"Cabecera Municipal de {nombre_cabecera}"
                        )
                    else:
                        dynamic_keywords = (
                            f"República de Colombia, Departamento {nombre_departamento}, "
                            f"Municipio de {nombre_municipio}, Cabecera Municipal de {nombre_cabecera}"
                        )
                else:
                    # Ej. Centro Poblado, Inspección, Corregimiento, etc.
                    dynamic_keywords = (
                        f"República de Colombia, Departamento {nombre_departamento}, "
                        f"Municipio de {nombre_municipio}, {tipo_centro} {nombre_cabecera}"
                    )

        kw_element = create_element(place_keywords, 'keyword')
        create_element(kw_element, 'gco:CharacterString', dynamic_keywords)
        arcpy.AddMessage(f"===================================================================")
        arcpy.AddMessage(f"✅ Palabras clave geográficas: {dynamic_keywords}")
        arcpy.AddMessage(f"===================================================================")
        # Configurar explícitamente como tipo "place"
        place_type_code = create_element(place_keywords, 'type')
        place_type_element = create_element(place_type_code, 'MD_KeywordTypeCode', 'place')
        place_type_element.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode')
        place_type_element.set('codeListValue', 'place')  # Esto es lo que establece el tipo como "place"
        place_type_element.set('codeSpace', 'ISOTC211/19115')

        # Agregar downoable data
        downoable_data = create_element(data_ident, 'descriptiveKeywords')
        downoable_data_kw = create_element(downoable_data, 'MD_Keywords')
        kw_element = create_element(downoable_data_kw, 'keyword')
        create_element(kw_element, 'gco:CharacterString', "Downloadable Data")
        kw_element_dw = create_element(downoable_data_kw, 'thesaurusName')
        kw_element_dw.set('uuidref', '723f6998-058e-11dc-8314-0800200c9a66')        
        
        # Descriptive Keywords-------------------------------
        # Keywords temáticas (las originales)
        kw_section = create_element(data_ident, 'descriptiveKeywords')
        keywords = create_element(kw_section, 'MD_Keywords')

        # Combinar todas las palabras clave en una sola cadena separada por comas
        keywords_text = ', '.join(MDT_KEYWORDS['temas'])

        # Crear solo un nodo <keyword> con todo el texto
        kw_element = create_element(keywords, 'keyword')
        create_element(kw_element, 'gco:CharacterString', keywords_text)


        # Tipo para keywords temáticas
        type_code = create_element(keywords, 'type')
        type_element = create_element(type_code, 'MD_KeywordTypeCode', 'theme')
        type_element.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode')
        type_element.set('codeListValue', 'theme')
        type_element.set('codeSpace', 'ISOTC211/19115')

        
        # Resource Constraints escala
        constraints = create_element(data_ident, 'resourceConstraints')
        md_constraints = create_element(constraints, 'MD_Constraints')
        
        use_limitation = create_element(md_constraints, 'useLimitation')
        create_element(use_limitation, 'gco:CharacterString', 
                      f'Producto generado para escalas iguales o menores a escala {escala}.')
        
        # Resource Constraints licencia
        constraints = create_element(data_ident, 'resourceConstraints')
        md_constraints = create_element(constraints, 'MD_Constraints')
        
        use_limitation = create_element(md_constraints, 'useLimitation')
        create_element(use_limitation, 'gco:CharacterString', 
                      f'Este producto adopta la licencia pública internacional de Reconocimiento-CompartirIgual 4.0 de Creative Commons, Creative Commons attribution – ShareAlike 4.0 Internacional. Por tal razón, nuevos productos y servicios derivados de su reutilización deben ser también licenciados bajo las mismas condiciones de uso y disponibilidad que habilitó la licencia antes mencionada. En todo caso el uso de la información será realizado por las partes de acuerdo con lo establecido en el artículo 61 de la Constitución Política, las Leyes 23 de 1982, 44 de 1993 y 565 de 2000 y, demás normas que las modifiquen, adicionen o aclaren.')
        
        # Añadir resolución espacial
        spatial_res = create_element(data_ident, 'spatialResolution')
        gco_res = create_element(spatial_res, 'MD_Resolution')
        distance = create_element(gco_res, 'distance')

        # Ajustar el valor de la distancia a metros y establecer el atributo uom sin namespace
        create_element(
            distance,
            'gco:Distance',
            text=f"{float(location_data['gsd']):.2f}",
            attributes={'uom': 'm'}
        )

        # Añadir characterSet
        char_set = create_element(data_ident, 'characterSet')
        char_code = create_element(char_set, 'MD_CharacterSetCode', text='utf8')
        char_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        char_code.set('codeListValue', 'utf8')
        char_code.set('codeSpace', 'ISOTC211/19115')

        # Extent
        extent_elem = create_element(data_ident, 'extent')
        ex_extent = create_element(extent_elem, 'EX_Extent')
        
        # Geographic Extent
        geo_elem = create_element(ex_extent, 'geographicElement')
        bbox = create_element(geo_elem, 'EX_GeographicBoundingBox')
        
        create_element(create_element(bbox, 'westBoundLongitude'), 'gco:Decimal', f"{extent.XMin:.6f}")
        create_element(create_element(bbox, 'eastBoundLongitude'), 'gco:Decimal', f"{extent.XMax:.6f}")
        create_element(create_element(bbox, 'southBoundLatitude'), 'gco:Decimal', f"{extent.YMin:.6f}")
        create_element(create_element(bbox, 'northBoundLatitude'), 'gco:Decimal', f"{extent.YMax:.6f}")
        
        # Temporal Extent
        temp_elem = create_element(ex_extent, 'temporalElement')
        ex_temp_ext = create_element(temp_elem, 'EX_TemporalExtent')
        extent = create_element(ex_temp_ext, 'extent')
        time_instant = create_element(extent, 'TimeInstant')
        time_instant.set('gml:id', f"ti_{identifier}")
        create_element(create_element(time_instant, 'timePosition'), 'gco:DateTime', 
                      location_data['fecha'].isoformat())
        
        # Topic Categories
        for category in MDT_KEYWORDS['categorias']:
            topic = create_element(data_ident, 'topicCategory')
            create_element(topic, 'MD_TopicCategoryCode', category)
        
        arcpy.AddMessage("Información de identificación agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de identificación: {str(e)}")
        raise

def MDT_add_spatial_representation_info(root, raster, extent):
    """Agrega información de representación espacial"""
    try:
        spatial = create_element(root, 'spatialRepresentationInfo')
        georect = create_element(spatial, 'MD_Georectified')
        
        # Number of Dimensions
        create_element(create_element(georect, 'numberOfDimensions'), 'gco:Integer', '2')
        
        # Axis Dimension Properties
        for dim_type in ['row', 'column']:
            axis_prop = create_element(georect, 'axisDimensionProperties')
            dim = create_element(axis_prop, 'MD_Dimension')
            
            dim_name = create_element(dim, 'dimensionName')
            code = create_element(dim_name, 'MD_DimensionNameTypeCode', dim_type)
            code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode')
            code.set('codeListValue', dim_type)
            code.set('codeSpace', 'ISOTC211/19115')
            
            size = raster.height if dim_type == 'row' else raster.width
            create_element(create_element(dim, 'dimensionSize'), 'gco:Integer', str(size))
            
            #Tamaño de la celda
            pixel_size = raster.meanCellWidth if hasattr(raster, "meanCellWidth") else 0.0
            # Redondeamos a 3 decimales y lo devolvemos como string
            pixel_size=f"{round(pixel_size, 3)}"

            res = create_element(dim, 'resolution')
            measure = create_element(res, 'gco:Measure', pixel_size)
            measure.set('uom', 'm')
        
        # Cell Geometry
        create_element(create_element(georect, 'cellGeometry'), 'gco:CharacterString', 'area')
        
        # Transformation Parameters Availability (¿Hay parámetros de transformación disponibles?)
        create_element(create_element(georect, 'transformationParameterAvailability'), 'gco:Boolean', 'true')

        # Transformation Dimension Description
        trans_dim = create_element(georect, 'transformationDimensionDescription')
        create_element(trans_dim, 'gco:CharacterString', 'Transformación Bilineal')

        # Check Points Availability (¿Hay puntos de verificación disponibles?)
        create_element(create_element(georect, 'checkPointAvailability'), 'gco:Boolean', 'true')

        #Check Points description
        create_element(create_element(georect, 'checkPointDescription'), 'gco:CharacterString', 'Pixel')

        # Corner Points y Center Point
        corners = [
            (extent.XMin, extent.YMax),  # Upper Left
            (extent.XMax, extent.YMax),  # Upper Right
            (extent.XMax, extent.YMin),  # Lower Right
            (extent.XMin, extent.YMin)   # Lower Left
        ]

        for x, y in corners:
            cp = create_element(georect, 'cornerPoints')
            gml_point = create_element(cp, 'gml:Point')
            gml_point.set('gml:id', f"ID{uuid.uuid4().hex.upper()}")
            gml_point.set('srsName', f"EPSG:{raster.spatialReference.factoryCode}")
            create_element(gml_point, 'gml:pos', f"{x:.3f} {y:.3f}")

        # Center Point
        center_x = (extent.XMin + extent.XMax) / 2
        center_y = (extent.YMin + extent.YMax) / 2
        center = create_element(georect, 'centerPoint')
        center_point = create_element(center, 'gml:Point')
        center_point.set('gml:id', f"ID{uuid.uuid4().hex.upper()}")
        center_point.set('srsName', f"EPSG:{raster.spatialReference.factoryCode}")
        create_element(center_point, 'gml:pos', f"{center_x:.3f} {center_y:.3f}")

        arcpy.AddMessage("Información de representación espacial agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando representación espacial: {str(e)}")
        raise

def MDT_add_reference_system_info(root, raster):
    """Agrega información del sistema de referencia"""
    try:
        ref_sys = create_element(root, 'referenceSystemInfo')
        md_ref = create_element(ref_sys, 'MD_ReferenceSystem')
        ref_id = create_element(md_ref, 'referenceSystemIdentifier')
        rs_id = create_element(ref_id, 'RS_Identifier')
        
        sr = raster.spatialReference
        
        if sr.factoryCode != 9377:
            arcpy.AddWarning("El sistema de referencia no es de origen nacional (EPSG:9377).")
        else:
            arcpy.AddMessage(f"✅ Sistema de referencia: {sr.name}")

        create_element(create_element(rs_id, 'code'), 'gco:CharacterString', str(sr.factoryCode))
        create_element(create_element(rs_id, 'codeSpace'), 'gco:CharacterString', 'EPSG')
        create_element(create_element(rs_id, 'version'), 'gco:CharacterString', '9.8.12(12.8.0)')
        
        arcpy.AddMessage("Información del sistema de referencia agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando sistema de referencia: {str(e)}")
        raise

def MDT_add_content_info(root, raster):
    """Agrega información sobre el contenido del raster"""
    try:
        
        content = create_element(root, 'contentInfo')
        img_desc = create_element(content, 'MD_ImageDescription')
        
        # Attribute Description - Cambiado a "Niveles Digitales" como en el ejemplo deseado
        attr_desc = create_element(img_desc, 'attributeDescription')
        create_element(attr_desc, 'gco:RecordType', 'Modelo Digital de Terreno')
        
        # Content Type
        content_type = create_element(img_desc, 'contentType')
        type_code = create_element(content_type, 'MD_CoverageContentTypeCode', 'image')
        type_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode')
        type_code.set('codeListValue', 'image')
        type_code.set('codeSpace', 'ISOTC211/19115')

        # Lista de nombres comunes de bandas (puedes ampliar o personalizar)
        nombres_bandas = ['Única', 'Verde', 'Azul', 'Banda_4', 'Banda_5', 'Banda_6', 'Banda_7', 'Banda_8']
        
        # Obtener número de bandas
        desc = arcpy.Describe(raster)
        num_bandas = desc.bandCount if hasattr(desc, "bandCount") else 1

        #Etiqueta dimension que contiene las bandas
        dimension = create_element(img_desc, 'dimension')
        for i in range(num_bandas):
            nombre_banda = nombres_bandas[i] if i < len(nombres_bandas) else f'Banda_{i+1}'

            # <dimension>
            md_band = create_element(dimension, 'MD_Band')

            # <sequenceIdentifier>
            seq_id = create_element(md_band, 'sequenceIdentifier')
            member_name = create_element(seq_id, 'gco:MemberName')
            a_name = create_element(member_name, 'gco:aName')
            create_element(a_name, 'gco:CharacterString', str(i + 1))  # Ej: "1"

            # <attributeType>
            attr_type = create_element(member_name, 'gco:attributeType')
            type_name = create_element(attr_type, 'gco:TypeName')
            create_element(create_element(type_name, 'gco:aName'), 'gco:CharacterString', nombre_banda)

            # Descriptor de la banda
            create_element(create_element(md_band, 'descriptor'), 'gco:CharacterString', f'Banda_{i+1}')

            # <units>
            units = create_element(md_band, 'units')
            unit_def = create_element(units, 'gml:UnitDefinition', attributes={'gml:id': f"ID{uuid.uuid4().hex.upper()}"})

            # <gml:identifier>
            create_element(unit_def, 'gml:identifier', 'Unified Code of Units of Measure', 
                        attributes={'codeSpace': 'GML_UomSymbol'})

            # <gml:catalogSymbol>
            create_element(unit_def, 'gml:catalogSymbol', 'bit_s', 
                        attributes={'codeSpace': 'http://aurora.regenstrief.org/UCUM'})


        # Añadir los elementos adicionales que aparecen en el ejemplo
        create_element(create_element(img_desc, 'triangulationIndicator'), 'gco:Boolean', 'false')
        create_element(create_element(img_desc, 'radiometricCalibrationDataAvailability'), 'gco:Boolean', 'false')
        create_element(create_element(img_desc, 'cameraCalibrationInformationAvailability'), 'gco:Boolean', 'false')
        create_element(create_element(img_desc, 'filmDistortionInformationAvailability'), 'gco:Boolean', 'false')
        create_element(create_element(img_desc, 'lensDistortionInformationAvailability'), 'gco:Boolean', 'false')
        
        arcpy.AddMessage("Información de contenido agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de contenido: {str(e)}")
        raise

def MDT_add_distribution_info(root, ORGANIZATION_INFO):
    """Agrega información de distribución con contacto del distribuidor"""

    try:
        dist = create_element(root, 'distributionInfo')
        md_dist = create_element(dist, 'MD_Distribution')
        
        # Formato
        dist_format = create_element(md_dist, 'distributionFormat')
        md_format = create_element(dist_format, 'MD_Format')
        create_element(create_element(md_format, 'name'), 'gco:CharacterString', 'TIFF')
        create_element(create_element(md_format, 'version'), 'gco:CharacterString', '1.0')

        # Contacto del distribuidor
        distributor = create_element(md_dist, 'distributor')
        md_distributor = create_element(distributor, 'MD_Distributor')
        dist_contact = create_element(md_distributor, 'distributorContact')
        responsible = create_element(dist_contact, 'CI_ResponsibleParty')

        create_element(create_element(responsible, 'organisationName'), 'gco:CharacterString',ORGANIZATION_INFO['name'])
        create_element(create_element(responsible, 'positionName'), 'gco:CharacterString',ORGANIZATION_INFO['position'])

        # Información de contacto
        contact_info = create_element(responsible, 'contactInfo')
        ci_contact = create_element(contact_info, 'CI_Contact')

        phone = create_element(ci_contact, 'phone')
        ci_phone = create_element(phone, 'CI_Telephone')
        create_element(create_element(ci_phone, 'voice'), 'gco:CharacterString', ORGANIZATION_INFO['phone'])

        address = create_element(ci_contact, 'address')
        ci_address = create_element(address, 'CI_Address')
        create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString',
                       'Carrera 30 # 48 - 51 – Sede Central')
        create_element(create_element(ci_address, 'city'), 'gco:CharacterString', ORGANIZATION_INFO['city'])
        create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', ORGANIZATION_INFO['state'])
        create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', ORGANIZATION_INFO['postal'])

        country = create_element(ci_address, 'country')
        create_element(country, 'Country', 'CO', {
            'codeList': 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm',
            'codeListValue': 'CO',
            'codeSpace': 'ISO3166-1'
        })

        create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString',ORGANIZATION_INFO['email'])

        create_element(create_element(ci_contact, 'hoursOfService'), 'gco:CharacterString',ORGANIZATION_INFO['hours'])
        create_element(create_element(ci_contact, 'contactInstructions'), 'gco:CharacterString',ORGANIZATION_INFO['instructions'])

        role = create_element(responsible, 'role')
        create_element(role, 'CI_RoleCode', 'distributor', {
            'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode',
            'codeListValue': 'distributor',
            'codeSpace': 'ISOTC211/19115'
        })     

        arcpy.AddMessage("Información de distribución agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de distribución: {str(e)}")
        raise

def MDT_add_data_quality_info(root, location_data, identifier):
    """Agrega información de calidad de datos"""
    try:
        quality = create_element(root, 'dataQualityInfo')
        dq_quality = create_element(quality, 'DQ_DataQuality')
        
        # Scope
        scope = create_element(dq_quality, 'scope')
        dq_scope = create_element(scope, 'DQ_Scope')
        level = create_element(dq_scope, 'level')
        scope_code = create_element(level, 'MD_ScopeCode', 'dataset')
        scope_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
        scope_code.set('codeListValue', 'dataset')
        scope_code.set('codeSpace', 'ISOTC211/19115')
        
        # Lineage
        lineage = create_element(dq_quality, 'lineage')
        li_lineage = create_element(lineage, 'LI_Lineage')
        statement = create_element(li_lineage, 'statement')

        def construir_descripcion_ubicacion(location_data):
            """Construye la descripción de ubicación según el tipo de centro poblado"""

            partes_ubicacion = []
            if location_data.get("tipo_centro") == "Cabecera Municipal":
                nombre_municipio = location_data.get("municipio", "")
                nombre_cabecera = location_data.get("centro_poblado", "")

                if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                else:
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                    partes_ubicacion.append(f"municipio de {nombre_municipio}")

                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            
            elif location_data.get("tipo_centro") == "Centro Poblado":
                if location_data.get("centro_poblado") and location_data.get("centro_poblado") != "Desconocido":
                    partes_ubicacion.append(f"del centro poblado {location_data.get('centro_poblado')}")
                # if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                #     partes_ubicacion.append(f"municipio de {location_data.get('municipio')}")
                # if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                #     partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            elif location_data.get("municipio") == "Desconocido":
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"del departamento {location_data.get('departamento')}")
                    
            elif location_data.get("centro_poblado") == "Desconocido":
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"del municipio de {location_data.get('municipio')}")
                # if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                #     partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            texto = ", ".join(partes_ubicacion)
            return texto
        
        descripcion_ubicacion = construir_descripcion_ubicacion(location_data)
        # Ejemplo: MDT1_Metadato_66045000_20200621.tif
        parts = identifier.split('_')
        gsd = parts[0].replace('MDT', '')  # 10
        code = parts[2]  # 66045000
        date_str = parts[3]  # 20200621
        # Construir el identificador
        identifier2 = f'MDT{gsd}_{code}_{date_str}'

        # Manejar plural de las unidades de malla
        if gsd == "1":
            unidad = "metro"
        else:
            unidad = "metros"

        statement_text = (
            f"El aseguramiento de la calidad se validó al 100% de los elementos contenidos en el "
            f"Modelo Digital de Terreno {identifier2} {descripcion_ubicacion}, el cual presenta una malla de {location_data['gsd']} {unidad} "
            f"y una extensión de {location_data['area_ha']:,.2f} hectáreas. "
            f"Se verificó el cumplimiento de los parámetros de calidad para modelos digitales de terreno de la Especificación Técnica "
            f"471-2020/529-2020/197-2022 en los elementos y subelementos de calidad, determinándose que el sistema de referencia cumple, "
            f"ya que tiene asignado MAGNA SIRGAS Origen-Nacional. Así mismo, cumple con los parámetros de totalidad (omisión, comisión), "
            f"exactitud en posición vertical, consistencia lógica, consistencia temporal y formato, lo cual permitió dar el concepto de APROBADO "
            f"para el MDT {descripcion_ubicacion}."
        )
        create_element(statement, 'gco:CharacterString', statement_text)

        arcpy.AddMessage("Información de calidad agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de calidad: {str(e)}")
        raise

def MDT_add_metadata_maintenance(root):
    """Agrega información de mantenimiento de metadatos"""
    try:
        maint = create_element(root, 'metadataMaintenance')
        md_maint = create_element(maint, 'MD_MaintenanceInformation')
        
        # Maintenance Frequency
        freq = create_element(md_maint, 'maintenanceAndUpdateFrequency')
        freq_code = create_element(freq, 'MD_MaintenanceFrequencyCode', 'asNeeded')
        freq_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode')
        freq_code.set('codeListValue', 'asNeeded')
        freq_code.set('codeSpace', 'ISOTC211/19115')
        
        arcpy.AddMessage("Información de mantenimiento agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de mantenimiento: {str(e)}")
        raise


# ==============================
# TOOLBOX
# ==============================

class Toolbox:
    def __init__(self):
        """Define la toolbox."""
        self.label = "Generación Automática de Metadatos - MRojas-Yquevedo"
        self.alias = "MetadataTIF"
        self.tools = [Metadato_MDT, Metadato_Orto]


# ==============================
# HERRAMIENTAS
# ==============================
class Metadato_MDT:
    def __init__(self):
        """Define la herramienta."""
        self.label = "Generación Automática de Metadato - MDT"
        self.description = "Genera el metadato XML conforme a NTC 4611 e ISO 19139."

    # ----------------------------------------------------------
    # PARÁMETROS
    # ----------------------------------------------------------
    def getParameterInfo(self):
        raster_path = arcpy.Parameter(
            displayName="Ruta del Raster",
            name="raster_path",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )

        output_folder = arcpy.Parameter(
            displayName="Ruta de Salida",
            name="out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )


        departamento = arcpy.Parameter(
            displayName="Departamento",
            name="departamento",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        try:
            departamento.filter.list = self.get_departamentos()
        except Exception:
            departamento.filter.list = []

        municipio = arcpy.Parameter(
            displayName="Municipio",
            name="municipio",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )
        municipio.filter.list = []
        municipio.parameterDependencies = ["departamento"]

        centro_poblado = arcpy.Parameter(
            displayName="Centro Poblado",
            name="centro_poblado",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )
        centro_poblado.filter.list = []
        centro_poblado.parameterDependencies = ["municipio"]

        fecha = arcpy.Parameter(
            displayName="Fecha",
            name="fecha",
            datatype="GPDate",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        boundary_fc = arcpy.Parameter(
            displayName="Límite del proyecto",
            name="shp",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        sensor = arcpy.Parameter(
            displayName="Sensor",
            name="sensor",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        puntos_lidar = arcpy.Parameter(
            displayName="Gererado con puntos LIDAR",
            name="LIDAR",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )

        #### Información de la organización
        name = arcpy.Parameter(
            displayName="Nombre de la Organización",
            name="name",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        position = arcpy.Parameter(
            displayName="Dependencia de la Organización",
            name="position",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        phone = arcpy.Parameter(
            displayName="Teléfono",
            name="phone",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        phone.value = "+57 (601)"
        
        address = arcpy.Parameter(
            displayName="Dirección",
            name="address",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )      

        city = arcpy.Parameter(
            displayName="Ciudad",
            name="city",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )    

        state = arcpy.Parameter(
            displayName="Departamento",
            name="state",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        postal = arcpy.Parameter(
            displayName="Código Postal",
            name="postal",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        ) 

        country = arcpy.Parameter(
            displayName="País",
            name="country",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        ) 
        country.value = "CO"

        email = arcpy.Parameter(
            displayName="Email",
            name="email",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        hours = arcpy.Parameter(
            displayName="Horario de Atención",
            name="hours",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        hours.value = "Lunes a viernes de XX:00 a.m. a XX:00 p.m"

        instructions = arcpy.Parameter(
            displayName="Instrucciones",
            name="instructions",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        instructions.value = "Abierto al público de lunes a viernes de XX:00 a.m. a XX:00 p.m."


        return [
            raster_path, output_folder, departamento, municipio, centro_poblado,
            fecha, boundary_fc, sensor, puntos_lidar, 
            name, position, phone, address, city,
            state, postal, country, email, hours, instructions
        ]

    # ----------------------------------------------------------
    # ACTUALIZACIÓN DE LISTAS
    # ----------------------------------------------------------
    def updateParameters(self, parameters):
        if parameters[2].value:
            parameters[3].filter.list = self.get_municipios(parameters[2].value)
        if parameters[3].value:
            parameters[4].filter.list = self.get_centros_poblados(parameters[3].value)

    # ----------------------------------------------------------
    # FUNCIONES AUXILIARES
    # ----------------------------------------------------------
    def get_departamentos(self):
        return [f"{k} - {v['Departamento']}" for k, v in dane_dict.items() if len(k) == 2]

    def get_municipios(self, departamento):
        pref = departamento.split(' - ')[0][:2]
        return [f"{k} - {v['Municipio']}" for k, v in dane_dict.items() if len(k) == 5 and k.startswith(pref)]

    def get_centros_poblados(self, municipio):
        pref = municipio.split(' - ')[0][:5]
        return [f"{k} - {v['Centro Poblado']}" for k, v in dane_dict.items() if len(k) > 5 and k.startswith(pref)]

    def isLicensed(self):
        return True

    # ----------------------------------------------------------
    # EJECUCIÓN
    # ----------------------------------------------------------
    def execute(self, parameters, messages):

        ## Parametros 
        raster_path = parameters[0].valueAsText
        output_folder = parameters[1].valueAsText
        departamento = parameters[2].valueAsText
        municipio = parameters[3].valueAsText
        centro_poblado = parameters[4].valueAsText
        fecha = parameters[5].value
        boundary_fc = parameters[6].valueAsText
        sensor = parameters[7].valueAsText
        puntos_lidar = parameters[8].valueAsText

        #Parametros de contacto
        # Constantes de la organización (Se usa para Organizacion, Citation y Metadata contacts)
        # Parámetros de contacto externo
        ORGANIZATION_INFO = {
            'role': 'originator',
            'name' : parameters[9].valueAsText,
            'position' : parameters[10].valueAsText,
            'phone' : parameters[11].valueAsText,
            'address' : parameters[12].valueAsText,
            'city' : parameters[13].valueAsText,
            'state' : parameters[14].valueAsText,
            'postal' : parameters[15].valueAsText,
            'country' : parameters[16].valueAsText,
            'email' : parameters[17].valueAsText,
            'hours' : parameters[18].valueAsText,
            'instructions' : parameters[19].valueAsText
        }

        EXTERNO = ORGANIZATION_INFO

        # Formatear fecha
        if isinstance(fecha, datetime):
            fecha_formateada = fecha.strftime("%Y%m%d")
        else:
            fecha_formateada = str(fecha)

        # DIVIPOLA
        if centro_poblado:
            divipola = centro_poblado.split(' - ')[0]
        elif municipio:
            divipola = municipio.split(' - ')[0]
        else:
            divipola = departamento.split(' - ')[0]
        
        # Cargar raster
        raster = arcpy.Raster(raster_path)

        #Manejo de GSD
        gsd_real = raster.meanCellWidth if hasattr(raster, "meanCellWidth") else 0.0  # GSD en metros
        gsd_real = round(gsd_real, 1)
        gsd = int(gsd_real)

        nuevo_nombre = f"MDT{gsd}_{divipola}_{fecha_formateada}"


        # Codificar
        arcpy.AddMessage(f"✅ Iniciando generación de metadatos para: {raster_path}")
        arcpy.AddMessage(f"✅ Codificación IGAC: {os.path.basename(raster_path)} → {nuevo_nombre}")

        #Calcular estadisticas del raster si no las tiene, necesario para content info.
        try: 
            arcpy.management.GetRasterProperties(raster_path, "MINIMUM")
            arcpy.AddMessage(f"El raster ya cuenta con estadisticas")
        except:
            arcpy.AddMessage(f"El raster no tiene estadísticas, calculando...")
            arcpy.management.CalculateStatistics(raster_path)
        
        # Obtener información espacial
        area_ha, extent, extent2 = get_spatial_info(boundary_fc, raster_path)
        
        # Extraer información del nombre del archivo
        raster_name = nuevo_nombre
        location_data = parse_filename(raster_name, dane_dict)
        location_data['area_ha'] = area_ha


        arcpy.AddMessage(f"Tamaño de pixel del raster: {gsd_real:.6f} metros")  # Mostrar con precisión


        # Asignar siempre el GSD real al diccionario
        location_data['gsd_nombre'] = location_data['gsd']
        location_data['gsd'] = str(int(round(gsd_real))) if gsd_real % 1 == 0 else str(round(gsd_real))


        ##################################################
        # INICIAR CREACION DE XML DE METADATO
        ##################################################

        #Crear esquema cascaron
        root = create_root_metadata()
        
        # Agregar las secciones de metadatos
        identifier = MDT_add_basic_metadata_sections(root, raster_name, location_data)
        MDT_add_contact_info(root, EXTERNO)
        MDT_add_identification_info(root, identifier, location_data, extent, area_ha, sensor, puntos_lidar, ORGANIZATION_INFO)
        MDT_add_spatial_representation_info(root, raster, extent2)
        MDT_add_reference_system_info(root, raster)
        MDT_add_content_info(root, raster)
        MDT_add_distribution_info(root, ORGANIZATION_INFO)
        MDT_add_data_quality_info(root, location_data, identifier)
        MDT_add_metadata_maintenance(root)
        
        # Guardar el archivo XML
        xml_entrada = save_metadata(root, output_folder, identifier)
        #Generar thumbnail
        ruta_thumbnail = generar_thumbnail(raster_path, output_folder)
        # Importar thumbnail y metadato
        importar_y_exportar_metadatos(raster_path, xml_entrada, xml_entrada, ruta_thumbnail)


#================================================================
#FUNCIONES PARA LA GENERACIÓN DE METADATOS PARA ORTOIMAGENES
#================================================================

def ORTO_add_basic_metadata_sections(root, filename, location_data):
    """Agrega secciones básicas de metadatos"""
    try:
        #Fileidentifier etiqueta
        # Ejemplo: Orto10_66045000_20200621.tif, resultado Orto10_Metadato_66045000_20200621.tif
        filename = filename.replace('.tif', '')  # quitar extensión si está
        parts = filename.split('_')
        
        if len(parts) < 3:
            raise ValueError("Formato de nombre de archivo incorrecto")
        
        gsd = location_data['gsd_nombre']

        # Extraer partes del nombre
        code = parts[1]
        date_str = parts[2]

        # Construir el identificador
        identifier = f'{gsd}_Metadato_{code}_{date_str}'

        arcpy.AddMessage(f"Identificador: {identifier}")

        id_element = create_element(root, 'fileIdentifier')
        create_element(id_element, 'gco:CharacterString', identifier) 

        
        # Language
        lang = create_element(root, 'language')
        code = create_element(lang, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')
        
        # Character Set
        char_set = create_element(root, 'characterSet')
        code = create_element(char_set, 'MD_CharacterSetCode', 'utf8')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        code.set('codeListValue', 'utf8')
        code.set('codeSpace', 'ISOTC211/19115')
        
        # Hierarchy Level
        hierarchy = create_element(root, 'hierarchyLevel')
        code = create_element(hierarchy, 'MD_ScopeCode', 'dataset')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
        code.set('codeListValue', 'dataset')
        code.set('codeSpace', 'ISOTC211/19115')
        
        # Hierarchy Level Name
        hierarchy_name = create_element(root, 'hierarchyLevelName')
        create_element(hierarchy_name, 'gco:CharacterString', 'dataset')
        
        # Date Stamp (Fecha de ultima actualización no automatica)
        # Fecha de publicación = 15 días después de la fecha de creación
        publication_datetime = datetime.now() + timedelta(days=15)
        publication_date_str = publication_datetime.strftime("%Y-%m-%d")
        create_element(create_element(root, 'dateStamp'), 'gco:Date', publication_date_str)
        
        # Metadata Standard
        create_element(create_element(root, 'metadataStandardName'), 'gco:CharacterString', 
                      'ISO 19139 Geographic Information - Metadata - Implementation Specification')
        create_element(create_element(root, 'metadataStandardVersion'), 'gco:CharacterString', '2007')
        
        # Locale
        locale = create_element(root, 'locale')
        pt_locale = create_element(locale, 'PT_Locale')
        
        lang_code = create_element(pt_locale, 'languageCode')
        code = create_element(lang_code, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')
        
        country = create_element(pt_locale, 'country')
        country_code = create_element(country, 'Country', 'CO')
        country_code.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_code.set('codeListValue', 'CO')
        country_code.set('codeSpace', 'ISO3166-1')
        
        char_enc = create_element(pt_locale, 'characterEncoding')
        enc_code = create_element(char_enc, 'MD_CharacterSetCode', 'utf8')
        enc_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        enc_code.set('codeListValue', 'utf8')
        enc_code.set('codeSpace', 'ISOTC211/19115')
                
        arcpy.AddMessage("Secciones básicas de metadatos agregadas correctamente")
        return identifier
    except Exception as e:
        arcpy.AddWarning(f"Error agregando secciones básicas: {str(e)}")
        raise

def ORTO_add_contact_info(root, EXTERNO):
    """Agrega información de contacto"""
    try:
        contact = create_element(root, 'contact')
        party = create_element(contact, 'CI_ResponsibleParty')
        
        # Agregar individualName antes de organisationName (orden es importante)
        #individual = create_element(party, 'individualName')
        #create_element(individual, 'gco:CharacterString', ORGANIZATION_INFO['name'])
        
        # El resto del código se mantiene igual...
        create_element(create_element(party, 'organisationName'), 'gco:CharacterString', EXTERNO['name'])
        create_element(create_element(party, 'positionName'), 'gco:CharacterString', EXTERNO['position'])
        
        # Información de contacto
        contact_info = create_element(party, 'contactInfo')
        ci_contact = create_element(contact_info, 'CI_Contact')
        
        # Teléfono
        phone = create_element(ci_contact, 'phone')
        tel = create_element(phone, 'CI_Telephone')
        voice = create_element(tel, 'voice')
        create_element(voice, 'gco:CharacterString', EXTERNO['phone'])
        
        # Dirección
        address = create_element(ci_contact, 'address')
        addr = create_element(address, 'CI_Address')
        
        delivery = create_element(addr, 'deliveryPoint')
        create_element(delivery, 'gco:CharacterString', EXTERNO['address'])
        
        city = create_element(addr, 'city')
        create_element(city, 'gco:CharacterString', EXTERNO['city'])
        
        area = create_element(addr, 'administrativeArea')
        create_element(area, 'gco:CharacterString', EXTERNO['state'])
        
        postal = create_element(addr, 'postalCode')
        create_element(postal, 'gco:CharacterString', EXTERNO['postal'])
        
        country = create_element(addr, 'country')
        country_code = create_element(country, 'Country', EXTERNO['country'])
        country_code.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_code.set('codeListValue', EXTERNO['country'])
        country_code.set('codeSpace', 'ISO3166-1')
        
        email = create_element(addr, 'electronicMailAddress')
        create_element(email, 'gco:CharacterString', EXTERNO['email'])
        
        # Rol
        role = create_element(party, 'role')
        code = create_element(role, 'CI_RoleCode', 'originator')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
        code.set('codeListValue', 'originator')
        code.set('codeSpace', 'ISOTC211/19115')
        
        arcpy.AddMessage("Información de contacto agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de contacto: {str(e)}")
        raise

def ORTO_add_identification_info(root, identifier, location_data, extent, area_ha, sensor, ORGANIZATION_INFO):
    """Agrega información de identificación del recurso"""
    try:
        ident = create_element(root, 'identificationInfo')
        data_ident = create_element(ident, 'MD_DataIdentification')
        
        # Citation
        citation = create_element(data_ident, 'citation')
        ci_citation = create_element(citation, 'CI_Citation')
        
        # Título
        title = create_element(ci_citation, 'title')

        # Determinar título dinámico según jerarquía disponible
        # Construcción del título
        if location_data['tipo_centro'] == "Cabecera Municipal":
            nombre_municipio = location_data['municipio']
            nombre_cabecera = location_data['centro_poblado']

            # Comparación normalizada para detectar si hay redundancia
            if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                title_text = (
                    f"Ortoimagen. Departamento {location_data['departamento']}. "
                    f"Cabecera Municipal de {nombre_cabecera}. "
                    f"GSD {location_data['gsd']} cm. "
                    f"Año {location_data['fecha'].year}"
                )
            else:
                title_text = (
                    f"Ortoimagen. Departamento {location_data['departamento']}. "
                    f"Municipio de {nombre_municipio}. "
                    f"Cabecera Municipal de {nombre_cabecera}. "
                    f"GSD {location_data['gsd']} cm. "
                    f"Año {location_data['fecha'].year}"
                )
        elif location_data['centro_poblado'] != "Desconocido":
            title_text = (
                f"Ortoimagen. Departamento {location_data['departamento']}. "
                f"Municipio de {location_data['municipio']}. "
                f"{location_data['tipo_centro']} de {location_data['centro_poblado']}. "
                f"GSD {location_data['gsd']} cm. "
                f"Año {location_data['fecha'].year}"
            )
        elif location_data['municipio'] != "Desconocido":
            title_text = (
                f"Ortoimagen. Departamento {location_data['departamento']}. "
                f"Municipio de {location_data['municipio']}. "
                f"GSD {location_data['gsd']} cm. "
                f"Año {location_data['fecha'].year}"
            )
        else:
            title_text = (
                f"Ortoimagen. Departamento {location_data['departamento']}. "
                f"GSD {location_data['gsd']} cm. "
                f"Año {location_data['fecha'].year}"
            )


        create_element(title, 'gco:CharacterString', title_text)

        # Titulo alternativo
        alt_title = create_element(ci_citation, 'alternateTitle')
        
        alternative_titulo = identifier.split('_')
        
        # Extraer partes del nombre
        code = alternative_titulo[2]
        date_str = alternative_titulo[3]
        gsd = alternative_titulo[0]

        # Construir el identificador
        identifieralt = f'{gsd}_{code}_{date_str}'

        create_element(alt_title, 'gco:CharacterString', identifieralt)
        
        # Fechas de creacion  y publicacion
        # Generar hora aleatoria para fecha de creación (horario laboral)
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        # Fecha de creación con hora aleatoria
        creation_datetime = datetime(
            location_data['fecha'].year,
            location_data['fecha'].month,
            location_data['fecha'].day,
            hour,
            minute,
            second
        )

        creation_date_str = creation_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        # Fecha de publicación = 15 días después de la fecha de creación
        publication_datetime = datetime.now() + timedelta(days=15)
        publication_date_str = publication_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        # === Fecha de creación ===
        date = create_element(ci_citation, 'date')
        ci_date = create_element(date, 'CI_Date')

        create_element(create_element(ci_date, 'date'), 'gco:DateTime', creation_date_str)

        date_type = create_element(ci_date, 'dateType')
        code = create_element(date_type, 'CI_DateTypeCode', 'creation')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode')
        code.set('codeListValue', 'creation')
        code.set('codeSpace', 'ISOTC211/19115')

        # === Fecha de publicación ===
        date = create_element(ci_citation, 'date')
        pu_date = create_element(date, 'CI_Date')

        create_element(create_element(pu_date, 'date'), 'gco:DateTime', publication_date_str)

        pu_date_type = create_element(pu_date, 'dateType')
        pu_code = create_element(pu_date_type, 'CI_DateTypeCode', 'publication')
        pu_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode')
        pu_code.set('codeListValue', 'publication')
        pu_code.set('codeSpace', 'ISOTC211/19115')

        # Dentro de ci_citation, presentation formats
        presentation_form = create_element(ci_citation, 'presentationForm')
        create_element(
            presentation_form,
            'CI_PresentationFormCode',
            text='imageDigital',
            attributes={
                'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_PresentationFormCode',
                'codeListValue': 'imageDigital',
                'codeSpace': 'ISOTC211/19115'
            }
        )


        #CREAR CONTACTO EN CITATION

        def crear_contacto_citation(ci_citation, diccionario):
            cited_party = create_element(ci_citation, 'citedResponsibleParty')
            responsible_party = create_element(cited_party, 'CI_ResponsibleParty')
            #create_element(create_element(responsible_party, 'individualName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
            create_element(create_element(responsible_party, 'organisationName'), 'gco:CharacterString', diccionario['name'])
            create_element(create_element(responsible_party, 'positionName'), 'gco:CharacterString', diccionario['position'])

            # Contact info
            contact_info = create_element(responsible_party, 'contactInfo')
            ci_contact = create_element(contact_info, 'CI_Contact')

            # Teléfono
            phone = create_element(ci_contact, 'phone')
            ci_phone = create_element(phone, 'CI_Telephone')
            create_element(create_element(ci_phone, 'voice'), 'gco:CharacterString', diccionario['phone'])

            # Dirección
            address = create_element(ci_contact, 'address')
            ci_address = create_element(address, 'CI_Address')

            create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString', diccionario['address'])
            create_element(create_element(ci_address, 'city'), 'gco:CharacterString', diccionario['city'])
            if diccionario.get('state'):
                create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', diccionario['state'])
            create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', diccionario['postal'])

            country = create_element(ci_address, 'country')
            country_el = create_element(country, 'Country', diccionario['country'])
            country_el.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
            country_el.set('codeListValue', diccionario['country'])
            country_el.set('codeSpace', 'ISO3166-1')

            create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString', diccionario['email'])

            # Horario
            create_element(create_element(ci_contact, 'hoursOfService'), 'gco:CharacterString', diccionario['hours'])
            create_element(create_element(ci_contact, 'contactInstructions'), 'gco:CharacterString',diccionario['instructions'])
            
            #Rol
            role = create_element(responsible_party, 'role')
            role_code = create_element(role, 'CI_RoleCode', diccionario['role'])
            role_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
            role_code.set('codeListValue', diccionario['role'])
            role_code.set('codeSpace', 'ISOTC211/19115')
        
        #Crear contacto de Rol originador
        crear_contacto_citation(ci_citation, ORGANIZATION_INFO )
        
        # Abstract ------------------------------------------------------------
        #Diccionario para manejar las escalas aplicables dependiendo del GSD

        def generar_abstract(location_data, area_ha, sensor):
            gsd = location_data["gsd"]
            escala = get_escala_por_gsd(gsd) 
            fecha_formateada = location_data["fecha"].strftime("%d de %B de %Y")
            
            partes_ubicacion = []
            if location_data.get("tipo_centro") == "Cabecera Municipal":
                nombre_municipio = location_data.get("municipio", "")
                nombre_cabecera = location_data.get("centro_poblado", "")

                if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                else:
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                    partes_ubicacion.append(f"municipio de {nombre_municipio}")

                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            
            elif location_data.get("tipo_centro") == "Centro Poblado":
                if location_data.get("centro_poblado") and location_data.get("centro_poblado") != "Desconocido":
                    partes_ubicacion.append(f"del centro poblado {location_data.get('centro_poblado')}")
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"municipio de {location_data.get('municipio')}")
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            elif location_data.get("municipio") == "Desconocido":
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"del departamento {location_data.get('departamento')}")

            elif location_data.get("centro_poblado") == "Desconocido":
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"del municipio de {location_data.get('municipio')}")
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            

            ubicacion = ", ".join(partes_ubicacion)

            abstract_text = (
                f"Ortoimagen compuesta de imágenes ortorectificadas, a las cuales se les aplicó un proceso de balance radiométrico y edición "
                f"de líneas de costura, garantizando la continuidad cromática y geométrica de los elementos. "
                f"Este producto contiene información {ubicacion}, República de Colombia. "
                f"Tiene un área de {area_ha:,.2f} hectáreas. "
                f"Cuenta con un GSD de {gsd} cm, aplicable para cartografía a escala {escala}, "
                f"los insumos fueron capturados con el sensor {sensor} el día {fecha_formateada}."
            )

            return abstract_text, escala


        abstract_text, escala = generar_abstract(location_data, area_ha, sensor)         
        create_element(create_element(data_ident, 'abstract'), 'gco:CharacterString', abstract_text)
        
        # Purpose
        purpose_text = ("Servir como insumo básico para la realización de estudios suburbanos y rurales como levantamientos catastrales,"
        " planificación de ordenación y manejo ambiental, ordenamiento territorial, deslindes, análisis espacial, ruteo, entre otros.")
        create_element(create_element(data_ident, 'purpose'), 'gco:CharacterString', purpose_text)
        
        # Status
        status = create_element(data_ident, 'status')
        code = create_element(status, 'MD_ProgressCode', 'completed')
        code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ProgressCode')
        code.set('codeListValue', 'completed')
        code.set('codeSpace', 'ISOTC211/19115')

        # Point of Contact
        poc = create_element(data_ident, 'pointOfContact')
        party = create_element(poc, 'CI_ResponsibleParty')

        #create_element(create_element(party, 'individualName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
        create_element(create_element(party, 'organisationName'), 'gco:CharacterString', ORGANIZATION_INFO['name'])
        create_element(create_element(party, 'positionName'), 'gco:CharacterString', ORGANIZATION_INFO['position'])

        # Contact Info
        contact_info = create_element(party, 'contactInfo')
        contact = create_element(contact_info, 'CI_Contact')

        # Teléfono
        phone = create_element(contact, 'phone')
        telephone = create_element(phone, 'CI_Telephone')
        create_element(create_element(telephone, 'voice'), 'gco:CharacterString', ORGANIZATION_INFO['phone'])

        # Dirección
        address = create_element(contact, 'address')
        ci_address = create_element(address, 'CI_Address')

        create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString', ORGANIZATION_INFO['address'])
        create_element(create_element(ci_address, 'city'), 'gco:CharacterString', ORGANIZATION_INFO['city'])
        create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', ORGANIZATION_INFO['state'])
        create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', ORGANIZATION_INFO['postal'])

        country = create_element(ci_address, 'country')
        country_el = create_element(country, 'Country', ORGANIZATION_INFO['country'])
        country_el.set('codeList', 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm')
        country_el.set('codeListValue', ORGANIZATION_INFO['country'])
        country_el.set('codeSpace', 'ISO3166-1')

        create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString', ORGANIZATION_INFO['email'])

        # Horario de atención
        create_element(create_element(contact, 'hoursOfService'), 'gco:CharacterString', ORGANIZATION_INFO['hours'])
        create_element(create_element(contact, 'contactInstructions'), 'gco:CharacterString',
                    ORGANIZATION_INFO['instructions'])

        # Rol
        role = create_element(party, 'role')
        role_code = create_element(role, 'CI_RoleCode', 'resourceProvider')
        role_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
        role_code.set('codeListValue', 'resourceProvider')
        role_code.set('codeSpace', 'ISOTC211/19115')
        
        
        # Language
        lang = create_element(data_ident, 'language')
        code = create_element(lang, 'LanguageCode', 'spa')
        code.set('codeList', 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        code.set('codeListValue', 'spa')
        code.set('codeSpace', 'ISO639-2')

        # Mantenimieto
        resource_maintenance = create_element(data_ident, 'resourceMaintenance')
        md_maintenance = create_element(resource_maintenance, 'MD_MaintenanceInformation')
        update_freq = create_element(md_maintenance, 'maintenanceAndUpdateFrequency')

        create_element(update_freq, 'MD_MaintenanceFrequencyCode', text='asNeeded', attributes={
            'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode',
            'codeListValue': 'asNeeded',
            'codeSpace': 'ISOTC211/19115'
        })

        
        # NUEVA SECCIÓN: Keywords geográficas con codeListValue="place"
        place_kw_section = create_element(data_ident, 'descriptiveKeywords')
        place_keywords = create_element(place_kw_section, 'MD_Keywords')

        nombre_departamento = location_data.get("departamento", "")
        nombre_municipio = location_data.get("municipio", "")
        nombre_cabecera = location_data.get("centro_poblado", "")
        tipo_centro = location_data.get("tipo_centro", "")

        if nombre_municipio == "Desconocido":
            dynamic_keywords = f"República de Colombia, Departamento {nombre_departamento}"
        else:
            if nombre_cabecera == "Desconocido":
                dynamic_keywords = f"República de Colombia, Departamento {nombre_departamento}, Municipio de {nombre_municipio}"
            else:
                if tipo_centro == "Cabecera Municipal":
                    if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                        dynamic_keywords = (
                            f"República de Colombia, Departamento {nombre_departamento}, "
                            f"Cabecera Municipal de {nombre_cabecera}"
                        )
                    else:
                        dynamic_keywords = (
                            f"República de Colombia, Departamento {nombre_departamento}, "
                            f"Municipio de {nombre_municipio}, Cabecera Municipal de {nombre_cabecera}"
                        )
                else:
                    # Ej. Centro Poblado, Inspección, Corregimiento, etc.
                    dynamic_keywords = (
                        f"República de Colombia, Departamento {nombre_departamento}, "
                        f"Municipio de {nombre_municipio}, {tipo_centro} {nombre_cabecera}"
                    )

        kw_element = create_element(place_keywords, 'keyword')
        create_element(kw_element, 'gco:CharacterString', dynamic_keywords)
        arcpy.AddMessage(f"===================================================================")
        arcpy.AddMessage(f"✅ Palabras clave geográficas: {dynamic_keywords}")
        arcpy.AddMessage(f"===================================================================")
        # Configurar explícitamente como tipo "place"
        place_type_code = create_element(place_keywords, 'type')
        place_type_element = create_element(place_type_code, 'MD_KeywordTypeCode', 'place')
        place_type_element.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode')
        place_type_element.set('codeListValue', 'place')  # Esto es lo que establece el tipo como "place"
        place_type_element.set('codeSpace', 'ISOTC211/19115')

        # Agregar downoable data
        downoable_data = create_element(data_ident, 'descriptiveKeywords')
        downoable_data_kw = create_element(downoable_data, 'MD_Keywords')
        kw_element = create_element(downoable_data_kw, 'keyword')
        create_element(kw_element, 'gco:CharacterString', "Downloadable Data")
        kw_element_dw = create_element(downoable_data_kw, 'thesaurusName')
        kw_element_dw.set('uuidref', '723f6998-058e-11dc-8314-0800200c9a66')
        
        # Descriptive Keywords-------------------------------
        # Keywords temáticas (las originales)
        kw_section = create_element(data_ident, 'descriptiveKeywords')
        keywords = create_element(kw_section, 'MD_Keywords')

        # Combinar todas las palabras clave en una sola cadena separada por comas
        keywords_text = ', '.join(ORTO_KEYWORDS['temas'])

        # Crear solo un nodo <keyword> con todo el texto
        kw_element = create_element(keywords, 'keyword')
        create_element(kw_element, 'gco:CharacterString', keywords_text)


        # Tipo para keywords temáticas
        type_code = create_element(keywords, 'type')
        type_element = create_element(type_code, 'MD_KeywordTypeCode', 'theme')
        type_element.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode')
        type_element.set('codeListValue', 'theme')
        type_element.set('codeSpace', 'ISOTC211/19115')

        
        # Resource Constraints escala
        constraints = create_element(data_ident, 'resourceConstraints')
        md_constraints = create_element(constraints, 'MD_Constraints')
        
        use_limitation = create_element(md_constraints, 'useLimitation')
        create_element(use_limitation, 'gco:CharacterString', 
                      f'Producto generado para escalas iguales o menores a escala {escala}.')
        
        # Resource Constraints licencia
        constraints = create_element(data_ident, 'resourceConstraints')
        md_constraints = create_element(constraints, 'MD_Constraints')
        
        use_limitation = create_element(md_constraints, 'useLimitation')
        create_element(use_limitation, 'gco:CharacterString', 
                      f'Este producto adopta la licencia pública internacional de Reconocimiento-CompartirIgual 4.0 de Creative Commons, Creative Commons attribution – ShareAlike 4.0 Internacional. Por tal razón, nuevos productos y servicios derivados de su reutilización deben ser también licenciados bajo las mismas condiciones de uso y disponibilidad que habilitó la licencia antes mencionada. En todo caso el uso de la información será realizado por las partes de acuerdo con lo establecido en el artículo 61 de la Constitución Política, las Leyes 23 de 1982, 44 de 1993 y 565 de 2000 y, demás normas que las modifiquen, adicionen o aclaren.')
        
        # Añadir resolución espacial
        spatial_res = create_element(data_ident, 'spatialResolution')
        gco_res = create_element(spatial_res, 'MD_Resolution')
        distance = create_element(gco_res, 'distance')

        # Ajustar el valor de la distancia a metros y establecer el atributo uom sin namespace
        create_element(
            distance,
            'gco:Distance',
            text=f"{float(location_data['gsd']) / 100:.2f}",
            attributes={'uom': 'm'}
        )

        # Añadir characterSet
        char_set = create_element(data_ident, 'characterSet')
        char_code = create_element(char_set, 'MD_CharacterSetCode', text='utf8')
        char_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        char_code.set('codeListValue', 'utf8')
        char_code.set('codeSpace', 'ISOTC211/19115')

        # Extent
        extent_elem = create_element(data_ident, 'extent')
        ex_extent = create_element(extent_elem, 'EX_Extent')
        
        # Geographic Extent
        geo_elem = create_element(ex_extent, 'geographicElement')
        bbox = create_element(geo_elem, 'EX_GeographicBoundingBox')
        
        create_element(create_element(bbox, 'westBoundLongitude'), 'gco:Decimal', f"{extent.XMin:.6f}")
        create_element(create_element(bbox, 'eastBoundLongitude'), 'gco:Decimal', f"{extent.XMax:.6f}")
        create_element(create_element(bbox, 'southBoundLatitude'), 'gco:Decimal', f"{extent.YMin:.6f}")
        create_element(create_element(bbox, 'northBoundLatitude'), 'gco:Decimal', f"{extent.YMax:.6f}")
        
        # Temporal Extent
        temp_elem = create_element(ex_extent, 'temporalElement')
        ex_temp_ext = create_element(temp_elem, 'EX_TemporalExtent')
        extent = create_element(ex_temp_ext, 'extent')
        time_instant = create_element(extent, 'TimeInstant')
        time_instant.set('gml:id', f"ti_{identifier}")
        create_element(create_element(time_instant, 'timePosition'), 'gco:DateTime', 
                      location_data['fecha'].isoformat())
        
        # Topic Categories
        for category in ORTO_KEYWORDS['categorias']:
            topic = create_element(data_ident, 'topicCategory')
            create_element(topic, 'MD_TopicCategoryCode', category)
        
        arcpy.AddMessage("Información de identificación agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de identificación: {str(e)}")
        raise

def ORTO_add_spatial_representation_info(root, raster, extent):
    """Agrega información de representación espacial"""
    try:
        spatial = create_element(root, 'spatialRepresentationInfo')
        georect = create_element(spatial, 'MD_Georectified')
        
        # Number of Dimensions
        create_element(create_element(georect, 'numberOfDimensions'), 'gco:Integer', '2')
        
        # Axis Dimension Properties
        for dim_type in ['row', 'column']:
            axis_prop = create_element(georect, 'axisDimensionProperties')
            dim = create_element(axis_prop, 'MD_Dimension')
            
            dim_name = create_element(dim, 'dimensionName')
            code = create_element(dim_name, 'MD_DimensionNameTypeCode', dim_type)
            code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode')
            code.set('codeListValue', dim_type)
            code.set('codeSpace', 'ISOTC211/19115')
            
            size = raster.height if dim_type == 'row' else raster.width
            create_element(create_element(dim, 'dimensionSize'), 'gco:Integer', str(size))
            
            #Tamaño de la celda
            pixel_size = raster.meanCellWidth if hasattr(raster, "meanCellWidth") else 0.0
            # Redondeamos a 3 decimales y lo devolvemos como string
            pixel_size=f"{round(pixel_size, 3)}"

            res = create_element(dim, 'resolution')
            measure = create_element(res, 'gco:Measure', pixel_size)
            measure.set('uom', 'm')
        
        # Cell Geometry
        create_element(create_element(georect, 'cellGeometry'), 'gco:CharacterString', 'area')
        
        # Transformation Parameters Availability (¿Hay parámetros de transformación disponibles?)
        create_element(create_element(georect, 'transformationParameterAvailability'), 'gco:Boolean', 'true')

        # Transformation Dimension Description
        trans_dim = create_element(georect, 'transformationDimensionDescription')
        create_element(trans_dim, 'gco:CharacterString', 'Transformación Bilineal')

        # Check Points Availability (¿Hay puntos de verificación disponibles?)
        create_element(create_element(georect, 'checkPointAvailability'), 'gco:Boolean', 'true')

        #Check Points description
        create_element(create_element(georect, 'checkPointDescription'), 'gco:CharacterString', 'Pixel')

        # Corner Points y Center Point
        corners = [
            (extent.XMin, extent.YMax),  # Upper Left
            (extent.XMax, extent.YMax),  # Upper Right
            (extent.XMax, extent.YMin),  # Lower Right
            (extent.XMin, extent.YMin)   # Lower Left
        ]

        for x, y in corners:
            cp = create_element(georect, 'cornerPoints')
            gml_point = create_element(cp, 'gml:Point')
            gml_point.set('gml:id', f"ID{uuid.uuid4().hex.upper()}")
            gml_point.set('srsName', f"EPSG:{raster.spatialReference.factoryCode}")
            create_element(gml_point, 'gml:pos', f"{x:.3f} {y:.3f}")

        # Center Point
        center_x = (extent.XMin + extent.XMax) / 2
        center_y = (extent.YMin + extent.YMax) / 2
        center = create_element(georect, 'centerPoint')
        center_point = create_element(center, 'gml:Point')
        center_point.set('gml:id', f"ID{uuid.uuid4().hex.upper()}")
        center_point.set('srsName', f"EPSG:{raster.spatialReference.factoryCode}")
        create_element(center_point, 'gml:pos', f"{center_x:.3f} {center_y:.3f}")

        arcpy.AddMessage("Información de representación espacial agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando representación espacial: {str(e)}")
        raise

def ORTO_add_reference_system_info(root, raster):
    """Agrega información del sistema de referencia"""
    try:
        ref_sys = create_element(root, 'referenceSystemInfo')
        md_ref = create_element(ref_sys, 'MD_ReferenceSystem')
        ref_id = create_element(md_ref, 'referenceSystemIdentifier')
        rs_id = create_element(ref_id, 'RS_Identifier')
        
        sr = raster.spatialReference
        if sr.factoryCode != 9377:
            arcpy.AddWarning("El sistema de referencia no es de origen nacional (EPSG:9377).")
        else:
            arcpy.AddMessage(f"✅ Sistema de referencia: {sr.name}")

        create_element(create_element(rs_id, 'code'), 'gco:CharacterString', str(sr.factoryCode))
        create_element(create_element(rs_id, 'codeSpace'), 'gco:CharacterString', 'EPSG')
        create_element(create_element(rs_id, 'version'), 'gco:CharacterString', '9.8.12(12.8.0)')
        
        arcpy.AddMessage("Información del sistema de referencia agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando sistema de referencia: {str(e)}")
        raise

def ORTO_add_content_info(root, raster, cloud_cover):
    """Agrega información sobre el contenido del raster"""
    try:
        
        content = create_element(root, 'contentInfo')
        img_desc = create_element(content, 'MD_ImageDescription')
        
        # Attribute Description - Cambiado a "Niveles Digitales" como en el ejemplo deseado
        attr_desc = create_element(img_desc, 'attributeDescription')
        create_element(attr_desc, 'gco:RecordType', 'Niveles Digitales')
        
        # Content Type
        content_type = create_element(img_desc, 'contentType')
        type_code = create_element(content_type, 'MD_CoverageContentTypeCode', 'image')
        type_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode')
        type_code.set('codeListValue', 'image')
        type_code.set('codeSpace', 'ISOTC211/19115')

        # Lista de nombres comunes de bandas (puedes ampliar o personalizar)
        nombres_bandas = ['Rojo', 'Verde', 'Azul', 'Infrarrojo', 'Banda_5', 'Banda_6', 'Banda_7', 'Banda_8']
        
        # Obtener número de bandas
        desc = arcpy.Describe(raster)
        num_bandas = desc.bandCount if hasattr(desc, "bandCount") else 1

        #Etiqueta dimension que contiene las bandas
        dimension = create_element(img_desc, 'dimension')
        for i in range(num_bandas):
            nombre_banda = nombres_bandas[i] if i < len(nombres_bandas) else f'Banda_{i+1}'

            # <dimension>
            md_band = create_element(dimension, 'MD_Band')

            # <sequenceIdentifier>
            seq_id = create_element(md_band, 'sequenceIdentifier')
            member_name = create_element(seq_id, 'gco:MemberName')
            a_name = create_element(member_name, 'gco:aName')
            create_element(a_name, 'gco:CharacterString', str(i + 1))  # Ej: "1"

            # <attributeType>
            attr_type = create_element(member_name, 'gco:attributeType')
            type_name = create_element(attr_type, 'gco:TypeName')
            create_element(create_element(type_name, 'gco:aName'), 'gco:CharacterString', nombre_banda)

            # Descriptor de la banda
            create_element(create_element(md_band, 'descriptor'), 'gco:CharacterString', f'Banda_{i+1}')

            # <units>
            units = create_element(md_band, 'units')
            unit_def = create_element(units, 'gml:UnitDefinition', attributes={'gml:id': f"ID{uuid.uuid4().hex[:8].upper()}"})

            # <gml:identifier>
            create_element(unit_def, 'gml:identifier', 'Unified Code of Units of Measure', 
                        attributes={'codeSpace': 'GML_UomSymbol'})

            # <gml:catalogSymbol>
            create_element(unit_def, 'gml:catalogSymbol', 'bit_s', 
                        attributes={'codeSpace': 'http://aurora.regenstrief.org/UCUM'})


        # Añadir los elementos adicionales que aparecen en el ejemplo
        if cloud_cover:
            create_element(create_element(img_desc, 'cloudCoverPercentage'), 'gco:Real', cloud_cover)
        create_element(create_element(img_desc, 'compressionGenerationQuantity'), 'gco:Integer', '85')
        create_element(create_element(img_desc, 'triangulationIndicator'), 'gco:Boolean', 'true')
        create_element(create_element(img_desc, 'radiometricCalibrationDataAvailability'), 'gco:Boolean', 'true')
        create_element(create_element(img_desc, 'cameraCalibrationInformationAvailability'), 'gco:Boolean', 'true')
        create_element(create_element(img_desc, 'filmDistortionInformationAvailability'), 'gco:Boolean', 'false')
        create_element(create_element(img_desc, 'lensDistortionInformationAvailability'), 'gco:Boolean', 'false')
        
        arcpy.AddMessage("Información de contenido agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de contenido: {str(e)}")
        raise

def ORTO_add_distribution_info(root, ORGANIZATION_INFO):
    """Agrega información de distribución con contacto del distribuidor"""

    try:
        dist = create_element(root, 'distributionInfo')
        md_dist = create_element(dist, 'MD_Distribution')
        
        # Formato
        dist_format = create_element(md_dist, 'distributionFormat')
        md_format = create_element(dist_format, 'MD_Format')
        create_element(create_element(md_format, 'name'), 'gco:CharacterString', 'TIFF')
        create_element(create_element(md_format, 'version'), 'gco:CharacterString', '1.0')

        # Contacto del distribuidor
        distributor = create_element(md_dist, 'distributor')
        md_distributor = create_element(distributor, 'MD_Distributor')
        dist_contact = create_element(md_distributor, 'distributorContact')
        responsible = create_element(dist_contact, 'CI_ResponsibleParty')

        create_element(create_element(responsible, 'organisationName'), 'gco:CharacterString',ORGANIZATION_INFO['name'])
        create_element(create_element(responsible, 'positionName'), 'gco:CharacterString',ORGANIZATION_INFO['position'])

        # Información de contacto
        contact_info = create_element(responsible, 'contactInfo')
        ci_contact = create_element(contact_info, 'CI_Contact')

        phone = create_element(ci_contact, 'phone')
        ci_phone = create_element(phone, 'CI_Telephone')
        create_element(create_element(ci_phone, 'voice'), 'gco:CharacterString', ORGANIZATION_INFO['phone'])

        address = create_element(ci_contact, 'address')
        ci_address = create_element(address, 'CI_Address')
        create_element(create_element(ci_address, 'deliveryPoint'), 'gco:CharacterString',
                       'Carrera 30 # 48 - 51 – Sede Central')
        create_element(create_element(ci_address, 'city'), 'gco:CharacterString', ORGANIZATION_INFO['city'])
        create_element(create_element(ci_address, 'administrativeArea'), 'gco:CharacterString', ORGANIZATION_INFO['state'])
        create_element(create_element(ci_address, 'postalCode'), 'gco:CharacterString', ORGANIZATION_INFO['postal'])

        country = create_element(ci_address, 'country')
        create_element(country, 'Country', 'CO', {
            'codeList': 'http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm',
            'codeListValue': 'CO',
            'codeSpace': 'ISO3166-1'
        })

        create_element(create_element(ci_address, 'electronicMailAddress'), 'gco:CharacterString',ORGANIZATION_INFO['email'])

        create_element(create_element(ci_contact, 'hoursOfService'), 'gco:CharacterString',ORGANIZATION_INFO['hours'])
        create_element(create_element(ci_contact, 'contactInstructions'), 'gco:CharacterString',ORGANIZATION_INFO['instructions'])

        role = create_element(responsible, 'role')
        create_element(role, 'CI_RoleCode', 'distributor', {
            'codeList': 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode',
            'codeListValue': 'distributor',
            'codeSpace': 'ISOTC211/19115'
        })     

        arcpy.AddMessage("Información de distribución agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de distribución: {str(e)}")
        raise

def ORTO_add_data_quality_info(root, location_data, identifier):
    """Agrega información de calidad de datos"""
    try:
        quality = create_element(root, 'dataQualityInfo')
        dq_quality = create_element(quality, 'DQ_DataQuality')
        
        # Scope
        scope = create_element(dq_quality, 'scope')
        dq_scope = create_element(scope, 'DQ_Scope')
        level = create_element(dq_scope, 'level')
        scope_code = create_element(level, 'MD_ScopeCode', 'dataset')
        scope_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
        scope_code.set('codeListValue', 'dataset')
        scope_code.set('codeSpace', 'ISOTC211/19115')
        
        # Lineage
        lineage = create_element(dq_quality, 'lineage')
        li_lineage = create_element(lineage, 'LI_Lineage')
        statement = create_element(li_lineage, 'statement')

        def construir_descripcion_ubicacion(location_data):
            """Construye la descripción de ubicación según el tipo de centro poblado"""

            partes_ubicacion = []
            if location_data.get("tipo_centro") == "Cabecera Municipal":
                nombre_municipio = location_data.get("municipio", "")
                nombre_cabecera = location_data.get("centro_poblado", "")

                if normalizar(nombre_municipio) == normalizar(nombre_cabecera):
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                else:
                    partes_ubicacion.append(f"de la cabecera municipal de {nombre_cabecera}")
                    partes_ubicacion.append(f"municipio de {nombre_municipio}")

                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"departamento {location_data.get('departamento')}")
            
            elif location_data.get("tipo_centro") == "Centro Poblado":
                if location_data.get("centro_poblado") and location_data.get("centro_poblado") != "Desconocido":
                    partes_ubicacion.append(f"del centro poblado {location_data.get('centro_poblado')}")
                # if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                #     partes_ubicacion.append(f"municipio de {location_data.get('municipio')}")
                # if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                #     partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            elif location_data.get("municipio") == "Desconocido":
                if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                    partes_ubicacion.append(f"del departamento {location_data.get('departamento')}")
                    
            elif location_data.get("centro_poblado") == "Desconocido":
                if location_data.get("municipio") and location_data.get("municipio") != "Desconocido":
                    partes_ubicacion.append(f"del municipio de {location_data.get('municipio')}")
                # if location_data.get("departamento") and location_data.get("departamento") != "Desconocido":
                #     partes_ubicacion.append(f"departamento {location_data.get('departamento')}")

            texto = ", ".join(partes_ubicacion)
            return texto
        
        descripcion_ubicacion = construir_descripcion_ubicacion(location_data)
        # Ejemplo: Orto10_Metadato_66045000_20200621.tif
        parts = identifier.split('_')
        gsd = parts[0].replace('Orto', '')  # 10
        code = parts[2]  # 66045000
        date_str = parts[3]  # 20200621
        # Construir el identificador
        identifier2 = f'Orto{gsd}_{code}_{date_str}'

        statement_text = (
            f"El aseguramiento de la calidad se realiza al 100% de los elementos contenidos en la "
            f"ortoimagen {identifier2} {descripcion_ubicacion}, la cual cuenta con un GSD de {location_data['gsd']} cm "
            f"y un área de {location_data['area_ha']:,.2f} hectáreas. "
            f"Se verificó el cumplimiento de los parámetros de calidad para ortoimágenes de la Especificación Técnica "
            f"471-2020/529-2020/197-2022 en los elementos y subelementos de calidad, determinándose que el sistema de referencia cumple, "
            f"ya que tiene asignado MAGNA SIRGAS Origen-Nacional. Así mismo, cumple con los parámetros de totalidad (omisión, comisión), "
            f"exactitud en posición horizontal, consistencia lógica, consistencia temporal y formato, lo cual permitió dar el concepto de APROBADO "
            f"para la ortoimagen {descripcion_ubicacion}."
        )
        create_element(statement, 'gco:CharacterString', statement_text)

        arcpy.AddMessage("Información de calidad agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de calidad: {str(e)}")
        raise

def ORTO_add_metadata_maintenance(root):
    """Agrega información de mantenimiento de metadatos"""
    try:
        maint = create_element(root, 'metadataMaintenance')
        md_maint = create_element(maint, 'MD_MaintenanceInformation')
        
        # Maintenance Frequency
        freq = create_element(md_maint, 'maintenanceAndUpdateFrequency')
        freq_code = create_element(freq, 'MD_MaintenanceFrequencyCode', 'asNeeded')
        freq_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode')
        freq_code.set('codeListValue', 'asNeeded')
        freq_code.set('codeSpace', 'ISOTC211/19115')
        
        arcpy.AddMessage("Información de mantenimiento agregada correctamente")
    except Exception as e:
        arcpy.AddWarning(f"Error agregando información de mantenimiento: {str(e)}")
        raise

class Metadato_Orto:
    def __init__(self):
        """Define la herramienta."""
        self.label = "Generación Automática de Metadato - Orto"
        self.description = "Genera el metadato XML conforme a NTC 4611 e ISO 19139."

    # ----------------------------------------------------------
    # PARÁMETROS
    # ----------------------------------------------------------
    def getParameterInfo(self):
        raster_path = arcpy.Parameter(
            displayName="Ruta del Raster",
            name="raster_path",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )

        output_folder = arcpy.Parameter(
            displayName="Ruta de Salida",
            name="out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )


        departamento = arcpy.Parameter(
            displayName="Departamento",
            name="departamento",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        try:
            departamento.filter.list = self.get_departamentos()
        except Exception:
            departamento.filter.list = []

        municipio = arcpy.Parameter(
            displayName="Municipio",
            name="municipio",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )
        municipio.filter.list = []
        municipio.parameterDependencies = ["departamento"]

        centro_poblado = arcpy.Parameter(
            displayName="Centro Poblado",
            name="centro_poblado",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )
        centro_poblado.filter.list = []
        centro_poblado.parameterDependencies = ["municipio"]

        fecha = arcpy.Parameter(
            displayName="Fecha",
            name="fecha",
            datatype="GPDate",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        boundary_fc = arcpy.Parameter(
            displayName="Límite del proyecto",
            name="shp",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        sensor = arcpy.Parameter(
            displayName="Sensor",
            name="sensor",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información del producto"
        )

        nubes = arcpy.Parameter(
            displayName="Porcentaje de nubes (%)",
            name="nubes",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input",
            category="Información del producto"
        )

        usar_layout_existente = arcpy.Parameter(
            displayName="Usar Layout Existente",
            name="layout",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )

        #### Información de la organización
        name = arcpy.Parameter(
            displayName="Nombre de la Organización",
            name="name",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        position = arcpy.Parameter(
            displayName="Dependencia de la Organización",
            name="position",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        phone = arcpy.Parameter(
            displayName="Teléfono",
            name="phone",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )

        phone.value = "+57 (601)"
        
        address = arcpy.Parameter(
            displayName="Dirección",
            name="address",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )      

        city = arcpy.Parameter(
            displayName="Ciudad",
            name="city",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )    

        state = arcpy.Parameter(
            displayName="Departamento",
            name="state",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        postal = arcpy.Parameter(
            displayName="Código Postal",
            name="postal",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        ) 

        country = arcpy.Parameter(
            displayName="País",
            name="country",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        ) 
        country.value = "CO"

        email = arcpy.Parameter(
            displayName="Email",
            name="email",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        hours = arcpy.Parameter(
            displayName="Horario de Atención",
            name="hours",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        hours.value = "Lunes a viernes de XX:00 a.m. a XX:00 p.m"

        instructions = arcpy.Parameter(
            displayName="Instrucciones",
            name="instructions",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Información de la Organización"
        )  

        instructions.value = "Abierto al público de lunes a viernes de XX:00 a.m. a XX:00 p.m."

        return [
            raster_path, output_folder, departamento, municipio, centro_poblado,
            fecha, boundary_fc, sensor, nubes, usar_layout_existente,
            name, position, phone, address, city,
            state, postal, country, email, hours, instructions
        ]

    # ----------------------------------------------------------
    # ACTUALIZACIÓN DE LISTAS
    # ----------------------------------------------------------
    def updateParameters(self, parameters):
        if parameters[2].value:
            parameters[3].filter.list = self.get_municipios(parameters[2].value)
        if parameters[3].value:
            parameters[4].filter.list = self.get_centros_poblados(parameters[3].value)

    # ----------------------------------------------------------
    # FUNCIONES AUXILIARES
    # ----------------------------------------------------------
    def get_departamentos(self):
        return [f"{k} - {v['Departamento']}" for k, v in dane_dict.items() if len(k) == 2]

    def get_municipios(self, departamento):
        pref = departamento.split(' - ')[0][:2]
        return [f"{k} - {v['Municipio']}" for k, v in dane_dict.items() if len(k) == 5 and k.startswith(pref)]

    def get_centros_poblados(self, municipio):
        pref = municipio.split(' - ')[0][:5]
        return [f"{k} - {v['Centro Poblado']}" for k, v in dane_dict.items() if len(k) > 5 and k.startswith(pref)]

    def isLicensed(self):
        return True

    # ----------------------------------------------------------
    # EJECUCIÓN
    # ----------------------------------------------------------
    def execute(self, parameters, messages):

        ## Parametros 
        raster_path = parameters[0].valueAsText
        output_folder = parameters[1].valueAsText
        departamento = parameters[2].valueAsText
        municipio = parameters[3].valueAsText
        centro_poblado = parameters[4].valueAsText
        fecha = parameters[5].value
        boundary_fc = parameters[6].valueAsText
        sensor = parameters[7].valueAsText
        cloud_cover = parameters[8].valueAsText
        usar_layout_existente = parameters[9].valueAsText

        if usar_layout_existente == None:
            usar_layout_existente = "false"
        else: 
            usar_layout_existente = "true"

        #Parametros de contacto
        # Constantes de la organización (Se usa para Organizacion, Citation y Metadata contacts)
        # Parámetros de contacto externo
        ORGANIZATION_INFO = {
            'role': 'originator',
            'name' : parameters[10].valueAsText,
            'position' : parameters[11].valueAsText,
            'phone' : parameters[12].valueAsText,
            'address' : parameters[13].valueAsText,
            'city' : parameters[14].valueAsText,
            'state' : parameters[15].valueAsText,
            'postal' : parameters[16].valueAsText,
            'country' : parameters[17].valueAsText,
            'email' : parameters[18].valueAsText,
            'hours' : parameters[19].valueAsText,
            'instructions' : parameters[20].valueAsText
        }

        EXTERNO = ORGANIZATION_INFO

        # Formatear fecha
        if isinstance(fecha, datetime):
            fecha_formateada = fecha.strftime("%Y%m%d")
        else:
            fecha_formateada = str(fecha)

        # DIVIPOLA
        if centro_poblado:
            divipola = centro_poblado.split(' - ')[0]
        elif municipio:
            divipola = municipio.split(' - ')[0]
        else:
            divipola = departamento.split(' - ')[0]
        
        # Cargar raster
        raster = arcpy.Raster(raster_path)

        #Manejo de GSD
        gsd_real = raster.meanCellWidth * 100 if hasattr(raster, "meanCellWidth") else 0.0  # Convertir a cm
        gsd_real = round(gsd_real, 1)
        gsd = int(gsd_real)

        nuevo_nombre = f"Orto{gsd}_{divipola}_{fecha_formateada}"


        # Codificar
        arcpy.AddMessage(f"✅ Iniciando generación de metadatos para: {raster_path}")
        arcpy.AddMessage(f"✅ Codificación IGAC: {os.path.basename(raster_path)} → {nuevo_nombre}")

        #Calcular estadisticas del raster si no las tiene, necesario para content info.
        try: 
            arcpy.management.GetRasterProperties(raster_path, "MINIMUM")
            arcpy.AddMessage(f"El raster ya cuenta con estadisticas")
        except:
            arcpy.AddMessage(f"El raster no tiene estadísticas, calculando...")
            arcpy.management.CalculateStatistics(raster_path)
        
        # Obtener información espacial
        area_ha, extent, extent2 = get_spatial_info(boundary_fc, raster_path)
        
        # Extraer información del nombre del archivo
        raster_name = nuevo_nombre
        location_data = parse_filename(raster_name, dane_dict)
        location_data['area_ha'] = area_ha


        arcpy.AddMessage(f"Tamaño de pixel del raster: {gsd_real:.6f} centimetros")  # Mostrar con precisión


        # Asignar siempre el GSD real al diccionario
        location_data['gsd_nombre'] = location_data['gsd']
        location_data['gsd'] = str(int(round(gsd_real))) if gsd_real % 1 == 0 else str(round(gsd_real))


        ##################################################
        # INICIAR CREACION DE XML DE METADATO
        ##################################################

        #Crear cascaron
        root = create_root_metadata()
        
        # Agregar las secciones de metadatos
        identifier = ORTO_add_basic_metadata_sections(root, raster_name, location_data)
        ORTO_add_contact_info(root, EXTERNO)
        ORTO_add_identification_info(root, identifier, location_data, extent, area_ha, sensor, ORGANIZATION_INFO)
        ORTO_add_spatial_representation_info(root, raster, extent2)
        ORTO_add_reference_system_info(root, raster)
        ORTO_add_content_info(root, raster, cloud_cover)
        ORTO_add_distribution_info(root, ORGANIZATION_INFO)
        ORTO_add_data_quality_info(root, location_data, identifier)
        ORTO_add_metadata_maintenance(root)
        
        # Guardar el archivo XML
        xml_entrada = save_metadata(root, output_folder, identifier)
        #Generar thumbnail
        ruta_thumbnail = generar_thumbnail(raster_path, output_folder, usar_layout_existente)
        # Importar thumbnail y metadato
        importar_y_exportar_metadatos(raster_path, xml_entrada, xml_entrada, ruta_thumbnail)
