import sys
import os
import types
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from ejercicio1_estructura_organizacional import OrganizacionNode
from ejercicio3_arbol_genealogico import PersonaNode
from ejercicio4_menu_aplicacion import MenuNode
from ejercicio5_dependencias_software import ModuloNode
from ejercicio6_autocompletado import Autocompletado
from ejercicio7_corrector_ortografico import CorrectorOrtografico
from ejercicio8_clasificador_intenciones import ClasificadorIntenciones
from ejercicio9_diccionario_multilenguaje import DiccionarioMultilenguaje
from ejercicio10_motor_busqueda import MotorBusqueda
from ejercicio11_registro_estudiantes import HashTable
from ejercicio12_comparacion_hash_vs_trie import Trie, HashDiccionario
from ejercicio13_heap_minimo import HeapMinimo
from ejercicio14_planificador_tareas import Tarea, PlanificadorTareas
from ejercicio15_simulacion_red import Paquete, SimuladorRed


class TestEjercicio1(unittest.TestCase):
    def setUp(self):
        self.raiz = OrganizacionNode("Rectoria")
        self.fac = OrganizacionNode("Ingenieria")
        self.prog = OrganizacionNode("Sistemas")
        self.fac.agregar_hijo(self.prog)
        self.raiz.agregar_hijo(self.fac)

    def test_agregar_hijo(self):
        assert "Ingenieria" in self.raiz.hijos

    def test_buscar_existente(self):
        assert self.raiz.buscar("Sistemas").nombre == "Sistemas"

    def test_buscar_inexistente(self):
        assert self.raiz.buscar("No existe") is None

    def test_buscar_raiz(self):
        assert self.raiz.buscar("Rectoria") is self.raiz

    def test_profundidad_raiz(self):
        assert self.raiz.profundidad("Rectoria") == 0

    def test_profundidad_hijo(self):
        assert self.raiz.profundidad("Ingenieria") == 1

    def test_profundidad_nieto(self):
        assert self.raiz.profundidad("Sistemas") == 2

    def test_profundidad_inexistente(self):
        assert self.raiz.profundidad("No existe") == -1

    def test_iter_recorre_todos(self):
        nombres = list(self.raiz)
        assert "Rectoria" in nombres
        assert "Ingenieria" in nombres
        assert "Sistemas" in nombres

    def test_iter_es_generator(self):
        assert isinstance(self.raiz.__iter__(), types.GeneratorType)


class TestEjercicio3(unittest.TestCase):
    def setUp(self):
        self.abuelo = PersonaNode("Abuelo")
        self.padre = PersonaNode("Padre")
        self.hijo = PersonaNode("Hijo")
        self.abuelo.agregar_hijo(self.padre)
        self.padre.agregar_hijo(self.hijo)

    def test_agregar_hijo_asigna_padre(self):
        assert self.padre.padre is self.abuelo

    def test_buscar_existente(self):
        assert self.abuelo.buscar("Hijo").nombre == "Hijo"

    def test_buscar_inexistente(self):
        assert self.abuelo.buscar("Nadie") is None

    def test_ancestros(self):
        ancestros = list(self.hijo.ancestros())
        assert ancestros == ["Padre", "Abuelo"]

    def test_ancestros_raiz_vacio(self):
        assert list(self.abuelo.ancestros()) == []

    def test_generaciones(self):
        assert self.abuelo.generaciones() == 2

    def test_iter_recorre_todos(self):
        nombres = list(self.abuelo)
        assert "Abuelo" in nombres
        assert "Padre" in nombres
        assert "Hijo" in nombres


class TestEjercicio4(unittest.TestCase):
    def setUp(self):
        self.raiz = MenuNode("Archivo")
        self.sub1 = MenuNode("Nuevo")
        self.sub2 = MenuNode("Abrir")
        self.raiz.agregar_subopcion(self.sub1)
        self.raiz.agregar_subopcion(self.sub2)

    def test_agregar_subopcion(self):
        assert "Nuevo" in self.raiz.subopciones

    def test_buscar_existente(self):
        assert self.raiz.buscar("Abrir").nombre == "Abrir"

    def test_buscar_inexistente(self):
        assert self.raiz.buscar("Guardar") is None

    def test_iter_recorre_todos(self):
        nombres = list(self.raiz)
        assert "Archivo" in nombres
        assert "Nuevo" in nombres
        assert "Abrir" in nombres


class TestEjercicio5(unittest.TestCase):
    def setUp(self):
        self.app = ModuloNode("app")
        self.db = ModuloNode("db")
        self.auth = ModuloNode("auth")
        self.app.agregar_dependencia(self.db)
        self.app.agregar_dependencia(self.auth)

    def test_agregar_dependencia(self):
        assert "db" in self.app.dependencias

    def test_grado(self):
        assert self.app.grado() == 2

    def test_buscar_existente(self):
        assert self.app.buscar("auth").nombre == "auth"

    def test_buscar_inexistente(self):
        assert self.app.buscar("cache") is None

    def test_impacto_de_cambio(self):
        resultado = list(self.app.impacto_de_cambio("app"))
        assert "app" in resultado

    def test_iter_recorre_todos(self):
        nombres = list(self.app)
        assert "app" in nombres
        assert "db" in nombres
        assert "auth" in nombres


class TestEjercicio6(unittest.TestCase):
    def setUp(self):
        self.ac = Autocompletado()
        for palabra in ["python", "pytest", "pip", "pandas", "java", "javascript"]:
            self.ac.insertar(palabra)

    def test_sugerencias_prefijo(self):
        resultado = list(self.ac.sugerencias("py"))
        assert "python" in resultado
        assert "pytest" in resultado

    def test_sugerencias_prefijo_inexistente(self):
        assert list(self.ac.sugerencias("xyz")) == []

    def test_sugerencias_es_generator(self):
        assert isinstance(self.ac.sugerencias("py"), types.GeneratorType)

    def test_buscar_prefijo_existente(self):
        assert self.ac.buscar_prefijo("pan") is not None

    def test_buscar_prefijo_inexistente(self):
        assert self.ac.buscar_prefijo("zzz") is None

    def test_palabra_completa_en_sugerencias(self):
        assert "python" in list(self.ac.sugerencias("python"))


class TestEjercicio7(unittest.TestCase):
    def setUp(self):
        self.corrector = CorrectorOrtografico()
        self.corrector.cargar_diccionario(["casa", "casas", "cama", "camara", "perro"])

    def test_verificar_correcta(self):
        assert self.corrector.verificar("casa") is True

    def test_verificar_incorrecta(self):
        assert self.corrector.verificar("csa") is False

    def test_verificar_prefijo_no_es_palabra(self):
        assert self.corrector.verificar("cas") is False

    def test_sugerencias_con_prefijo(self):
        resultado = list(self.corrector.sugerencias("cas"))
        assert "casa" in resultado
        assert "casas" in resultado

    def test_sugerencias_prefijo_inexistente(self):
        assert list(self.corrector.sugerencias("xyz")) == []

    def test_sugerencias_es_generator(self):
        assert isinstance(self.corrector.sugerencias("ca"), types.GeneratorType)


class TestEjercicio8(unittest.TestCase):
    def setUp(self):
        self.clf = ClasificadorIntenciones()
        self.clf.registrar_palabra("comprar", "compra")
        self.clf.registrar_palabra("precio", "compra")
        self.clf.registrar_palabra("ayuda", "soporte")
        self.clf.registrar_palabra("error", "soporte")

    def test_clasificar_una_intencion(self):
        resultado = self.clf.clasificar("quiero comprar algo")
        assert resultado.get("compra", 0) >= 1

    def test_clasificar_multiples_intenciones(self):
        resultado = self.clf.clasificar("comprar precio ayuda")
        assert resultado["compra"] == 2
        assert resultado["soporte"] == 1

    def test_clasificar_sin_coincidencias(self):
        resultado = self.clf.clasificar("hola mundo")
        assert resultado == {}

    def test_sugerencias_prefijo(self):
        resultado = list(self.clf.sugerencias_prefijo("comp"))
        assert "comprar" in resultado

    def test_sugerencias_prefijo_vacio(self):
        assert list(self.clf.sugerencias_prefijo("zzz")) == []


class TestEjercicio9(unittest.TestCase):
    def setUp(self):
        self.dic = DiccionarioMultilenguaje()
        self.dic.insertar("casa", "ingles", "house")
        self.dic.insertar("casa", "frances", "maison")
        self.dic.insertar("perro", "ingles", "dog")

    def test_traducir_existente(self):
        assert self.dic.traducir("casa", "ingles") == "house"

    def test_traducir_otro_idioma(self):
        assert self.dic.traducir("casa", "frances") == "maison"

    def test_traducir_idioma_inexistente(self):
        assert self.dic.traducir("casa", "aleman") is None

    def test_traducir_palabra_inexistente(self):
        assert self.dic.traducir("gato", "ingles") is None

    def test_palabras_por_prefijo(self):
        resultado = list(self.dic.palabras_por_prefijo("ca"))
        assert "casa" in resultado

    def test_buscar_existente(self):
        assert self.dic.buscar("perro") is not None

    def test_buscar_inexistente(self):
        assert self.dic.buscar("gato") is None


class TestEjercicio10(unittest.TestCase):
    def setUp(self):
        self.motor = MotorBusqueda()
        self.motor.indexar("python tutorial", 10)
        self.motor.indexar("python avanzado", 20)
        self.motor.indexar("java basico", 5)

    def test_buscar_prefijo_existente(self):
        resultados = list(self.motor.buscar("python"))
        assert len(resultados) >= 1

    def test_buscar_prefijo_inexistente(self):
        resultados = list(self.motor.buscar("rust"))
        assert resultados == []

    def test_resultado_mas_relevante_primero(self):
        motor = MotorBusqueda()
        motor.indexar("abc", 5)
        motor.indexar("abc", 20)
        resultados = list(motor.buscar("abc"))
        prioridades = [r.prioridad for r in resultados]
        assert prioridades == sorted(prioridades, reverse=True)

    def test_buscar_es_generator(self):
        assert isinstance(self.motor.buscar("py"), types.GeneratorType)


class TestEjercicio11(unittest.TestCase):
    def setUp(self):
        self.tabla = HashTable(capacidad=5)
        self.tabla["EST001"] = "Ana Garcia"
        self.tabla["EST002"] = "Carlos Ruiz"

    def test_setitem_getitem(self):
        assert self.tabla["EST001"] == "Ana Garcia"

    def test_actualizar_valor(self):
        self.tabla["EST001"] = "Ana Garcia H."
        assert self.tabla["EST001"] == "Ana Garcia H."

    def test_getitem_inexistente(self):
        with self.assertRaises(KeyError):
            _ = self.tabla["NOEXISTE"]

    def test_delitem(self):
        del self.tabla["EST001"]
        assert "EST001" not in self.tabla

    def test_delitem_inexistente(self):
        with self.assertRaises(KeyError):
            del self.tabla["NOEXISTE"]

    def test_contains(self):
        assert "EST002" in self.tabla
        assert "EST999" not in self.tabla

    def test_redimensionar_automatico(self):
        tabla = HashTable(capacidad=2)
        for i in range(10):
            tabla[f"K{i}"] = f"V{i}"
        for i in range(10):
            assert tabla[f"K{i}"] == f"V{i}"

    def test_items(self):
        pares = dict(self.tabla.items())
        assert pares["EST001"] == "Ana Garcia"


class TestEjercicio12(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.hash_dic = HashDiccionario()
        for p in ["python", "pytest", "pandas", "java"]:
            self.trie.insertar(p)
            self.hash_dic.insertar(p)

    def test_trie_buscar_existente(self):
        assert self.trie.buscar("python") is True

    def test_trie_buscar_inexistente(self):
        assert self.trie.buscar("ruby") is False

    def test_trie_buscar_prefijo_existente(self):
        assert self.trie.buscar_prefijo("py") is True

    def test_trie_buscar_prefijo_inexistente(self):
        assert self.trie.buscar_prefijo("zzz") is False

    def test_hash_buscar_existente(self):
        assert self.hash_dic.buscar("java") is True

    def test_hash_buscar_inexistente(self):
        assert self.hash_dic.buscar("go") is False

    def test_hash_buscar_prefijo_existente(self):
        assert self.hash_dic.buscar_prefijo("pan") is True

    def test_hash_buscar_prefijo_inexistente(self):
        assert self.hash_dic.buscar_prefijo("zzz") is False


class TestEjercicio13(unittest.TestCase):
    def setUp(self):
        self.heap = HeapMinimo()

    def test_insertar_y_ver_minimo(self):
        self.heap.insertar(5)
        self.heap.insertar(2)
        self.heap.insertar(8)
        assert self.heap.ver_minimo() == 2

    def test_extraer_minimo_orden(self):
        for v in [5, 2, 8, 1, 9]:
            self.heap.insertar(v)
        assert self.heap.extraer_minimo() == 1
        assert self.heap.extraer_minimo() == 2

    def test_extraer_vacio_lanza_error(self):
        with self.assertRaises(IndexError):
            self.heap.extraer_minimo()

    def test_ver_minimo_vacio(self):
        assert self.heap.ver_minimo() is None

    def test_construir(self):
        self.heap.construir([9, 3, 7, 1, 5])
        assert self.heap.extraer_minimo() == 1

    def test_len(self):
        self.heap.insertar(1)
        self.heap.insertar(2)
        assert len(self.heap) == 2


class TestEjercicio14(unittest.TestCase):
    def setUp(self):
        self.planificador = PlanificadorTareas()

    def test_agregar_y_ejecutar(self):
        self.planificador.agregar_tarea(Tarea("backup", 3))
        self.planificador.agregar_tarea(Tarea("critico", 1))
        primera = self.planificador.ejecutar_siguiente()
        assert primera.prioridad == 1

    def test_ejecutar_vacio_lanza_error(self):
        with self.assertRaises(IndexError):
            self.planificador.ejecutar_siguiente()

    def test_ver_siguiente_vacio_lanza_error(self):
        with self.assertRaises(IndexError):
            self.planificador.ver_siguiente()

    def test_ver_siguiente_no_extrae(self):
        self.planificador.agregar_tarea(Tarea("t", 1))
        self.planificador.ver_siguiente()
        assert self.planificador.tareas_pendientes() == 1

    def test_tareas_pendientes(self):
        for i in range(4):
            self.planificador.agregar_tarea(Tarea(f"t{i}", i))
        assert self.planificador.tareas_pendientes() == 4

    def test_lt_operator(self):
        t1 = Tarea("urgente", 1)
        t2 = Tarea("normal", 3)
        assert t1 < t2

    def test_orden_prioridad_correcto(self):
        self.planificador.agregar_tarea(Tarea("baja", 5))
        self.planificador.agregar_tarea(Tarea("alta", 1))
        self.planificador.agregar_tarea(Tarea("media", 3))
        prioridades = [self.planificador.ejecutar_siguiente().prioridad for _ in range(3)]
        assert prioridades == sorted(prioridades)


class TestEjercicio15(unittest.TestCase):
    def setUp(self):
        self.red = SimuladorRed(ancho_banda=100)

    def test_recibir_y_transmitir(self):
        self.red.recibir_paquete(Paquete("p1", 2, 50))
        self.red.recibir_paquete(Paquete("p2", 1, 30))
        primero = self.red.transmitir_siguiente()
        assert primero.prioridad == 1

    def test_transmitir_vacio_lanza_error(self):
        with self.assertRaises(IndexError):
            self.red.transmitir_siguiente()

    def test_ver_siguiente_vacio_lanza_error(self):
        with self.assertRaises(IndexError):
            self.red.ver_siguiente()

    def test_paquetes_pendientes(self):
        self.red.recibir_paquete(Paquete("p1", 1, 10))
        self.red.recibir_paquete(Paquete("p2", 2, 20))
        assert self.red.paquetes_pendientes() == 2

    def test_transmitir_agrega_a_transmitidos(self):
        self.red.recibir_paquete(Paquete("p1", 1, 10))
        self.red.transmitir_siguiente()
        assert len(self.red.transmitidos) == 1

    def test_orden_prioridad(self):
        self.red.recibir_paquete(Paquete("p1", 3, 10))
        self.red.recibir_paquete(Paquete("p2", 1, 10))
        self.red.recibir_paquete(Paquete("p3", 2, 10))
        prioridades = [self.red.transmitir_siguiente().prioridad for _ in range(3)]
        assert prioridades == sorted(prioridades)

    def test_lt_operator(self):
        p1 = Paquete("p1", 1, 10)
        p2 = Paquete("p2", 3, 10)
        assert p1 < p2


if __name__ == "__main__":
    unittest.main()
