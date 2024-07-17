import cv2
import face_recognition as fr
import numpy as np
from Figura import Figura


class SistemaReconocimientoFacial:
    def __init__(self):
        self.caras_codificadas = []
        self.nombres_caras = []

    def agregar_cara(self, imagen, nombre):

        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        codificaciones = fr.face_encodings(imagen_rgb)[0]

        self.caras_codificadas.append(codificaciones)
        self.nombres_caras.append(nombre)

    def tomar_foto(self):

        cap = cv2.VideoCapture(0)
        exito, img = cap.read()
        cap.release()
        if not exito:
            raise Exception("No se pudo tomar la foto")
        return img

    def reconocer_cara(self, img):
        # Detectar ubicaciones de caras en la imagen
        ubicaciones_caras = fr.face_locations(img)
        # Obtener las codificaciones faciales de las caras detectadas
        codificaciones_caras = fr.face_encodings(img, known_face_locations=ubicaciones_caras)
        return ubicaciones_caras, codificaciones_caras

    def encontrar_coincidencias(self, codificaciones_caras):
        coincidencias = []
        distancias = []
        for codificacion in codificaciones_caras:
            # Comparar las caras detectadas con las almacenadas
            coincidencia = fr.compare_faces(self.caras_codificadas, codificacion, 0.6)
            distancia = fr.face_distance(self.caras_codificadas, codificacion)
            coincidencias.append(coincidencia)
            distancias.append(distancia)
        return coincidencias, distancias

    def obtener_mejor_indice_coincidencia(self, distancias):
        if len(distancias) > 0:

            return np.argmin(distancias)
        return None

    def dibujar_figura(self, img, ubicacion_cara, tipo_figura):

        arriba, derecha, abajo, izquierda = ubicacion_cara
        centro_x, centro_y = (izquierda + derecha) // 2, (arriba + abajo) // 2
        radio = (derecha - izquierda) // 2

        figura = Figura(tipo_figura, radio)

        if tipo_figura == "circular":
            cv2.circle(img, (centro_x, centro_y), radio, (0, 255, 0), 2)
        elif tipo_figura == "esferica":
            cv2.circle(img, (centro_x, centro_y), radio, (0, 255, 0), 2)
        else:
            raise ValueError("Tipo de figura no reconocido. Use 'circular' o 'esferica'.")

        area = figura.calcular_area()
        volumen = figura.calcular_volumen()

        print(f"Área de la figura ({tipo_figura}): {area}")
        print(f"Volumen de la figura ({tipo_figura}): {volumen}")

    def ejecutar(self):
        img = self.tomar_foto()
        ubicaciones_caras, codificaciones_caras = self.reconocer_cara(img)

        if len(codificaciones_caras) == 0:
            print("No se encontraron caras")
            return

        coincidencias, distancias = self.encontrar_coincidencias(codificaciones_caras)
        mejor_indice_coincidencia = self.obtener_mejor_indice_coincidencia(distancias[0])

        if mejor_indice_coincidencia is not None and distancias[0][mejor_indice_coincidencia] < 0.6:
            nombre = self.nombres_caras[mejor_indice_coincidencia]
            print(f"Bienvenido {nombre}")
        else:
            print("No se encontró ninguna coincidencia")

        tipo_figura = "esferica"
        self.dibujar_figura(img, ubicaciones_caras[0], tipo_figura)

        cv2.imshow("Foto del Empleado", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":

    srf = SistemaReconocimientoFacial()

    srf.ejecutar()


