import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ejercicio1_arbol_nario import OrganizacionNode
from ejercicio2_trie import Trie
from ejercicio3_hash_table import HashTable, Estudiante
from ejercicio4_priority_queue import Tarea, PlanificadorKernel, Prioridad


class TestOrganizacionNode:
    def setup_method(self):
        self.rectoria = OrganizacionNode("Rectoria")
        self.fac_ing = OrganizacionNode("Facultad de Ingenieria")
        self.prog_sistemas = OrganizacionNode("Ing. Sistemas")
        self.fac_ing.agregar_hijo(self.prog_sistemas)
        self.rectoria.agregar_hijo(self.fac_ing)

    def test_agregar_hijo_exitoso(self):
        fac = OrganizacionNode("Nueva Facultad")
        self.rectoria.agregar_hijo(fac)
        assert "Nueva Facultad" in self.rectoria.hijos

    def test_agregar_hijo_duplicado_lanza_error(self):
        with pytest.raises(ValueError):
            self.rectoria.agregar_hijo(OrganizacionNode("Facultad de Ingenieria"))

    def test_buscar_existente(self):
        resultado = self.rectoria.buscar("Ing. Sistemas")
        assert resultado is not None
        assert resultado.nombre == "Ing. Sistemas"

    def test_buscar_inexistente(self):
        assert self.rectoria.buscar("No existe") is None

    def test_buscar_raiz(self):
        assert self.rectoria.buscar("Rectoria") is self.rectoria

    def test_eliminar_hijo_exitoso(self):
        self.rectoria.eliminar_hijo("Facultad de Ingenieria")
        assert "Facultad de Ingenieria" not in self.rectoria.hijos

    def test_eliminar_hijo_inexistente_lanza_error(self):
        with pytest.raises(KeyError):
            self.rectoria.eliminar_hijo("No existe")

    def test_iter_recorre_todos_los_nodos(self):
        nombres = [n.nombre for n in self.rectoria]
        assert "Rectoria" in nombres
        assert "Facultad de Ingenieria" in nombres
        assert "Ing. Sistemas" in nombres

    def test_iter_cantidad_nodos(self):
        assert len(list(self.rectoria)) == 3

    def test_acceso_hijos_O1(self):
        assert self.rectoria.hijos.get("Facultad de Ingenieria") is self.fac_ing


class TestTrie:
    def setup_method(self):
        self.trie = Trie()
        for cmd in ["git commit", "git clone", "git checkout", "docker run", "docker build"]:
            self.trie.insertar(cmd)

    def test_insertar_y_buscar(self):
        assert self.trie.buscar("git commit") is True

    def test_buscar_inexistente(self):
        assert self.trie.buscar("git xyz") is False

    def test_buscar_prefijo_no_es_palabra(self):
        assert self.trie.buscar("git") is False

    def test_sugerir_prefijo_existente(self):
        sugerencias = list(self.trie.sugerir("git"))
        assert len(sugerencias) == 3
        assert "git commit" in sugerencias

    def test_sugerir_prefijo_inexistente(self):
        assert list(self.trie.sugerir("xyz")) == []

    def test_sugerir_retorna_generator(self):
        import types
        assert isinstance(self.trie.sugerir("git"), types.GeneratorType)

    def test_insertar_duplicado_no_aumenta_len(self):
        tam_antes = len(self.trie)
        self.trie.insertar("git commit")
        assert len(self.trie) == tam_antes

    def test_len_correcto(self):
        assert len(self.trie) == 5

    def test_contains(self):
        assert "docker run" in self.trie
        assert "npm install" not in self.trie

    def test_eliminar_palabra(self):
        self.trie.eliminar("git commit")
        assert self.trie.buscar("git commit") is False

    def test_tiene_prefijo(self):
        assert self.trie.tiene_prefijo("doc") is True
        assert self.trie.tiene_prefijo("xyz") is False

    def test_insertar_vacia_lanza_error(self):
        with pytest.raises(ValueError):
            self.trie.insertar("")


class TestHashTable:
    def setup_method(self):
        self.tabla = HashTable(capacidad=4)
        self.est1 = Estudiante("EST001", "Ana Garcia", "Ing. Sistemas", 4)
        self.est2 = Estudiante("EST002", "Carlos Ruiz", "Matematicas", 2)
        self.tabla["EST001"] = self.est1
        self.tabla["EST002"] = self.est2

    def test_setitem_y_getitem(self):
        assert self.tabla["EST001"] == self.est1

    def test_getitem_inexistente_lanza_keyerror(self):
        with pytest.raises(KeyError):
            _ = self.tabla["INEXISTENTE"]

    def test_actualizar_valor(self):
        nuevo = Estudiante("EST001", "Ana Garcia H.", "Ing. Sistemas", 5)
        self.tabla["EST001"] = nuevo
        assert self.tabla["EST001"].nombre == "Ana Garcia H."

    def test_delitem_exitoso(self):
        del self.tabla["EST001"]
        assert "EST001" not in self.tabla

    def test_delitem_inexistente_lanza_keyerror(self):
        with pytest.raises(KeyError):
            del self.tabla["INEXISTENTE"]

    def test_contains(self):
        assert "EST001" in self.tabla
        assert "EST999" not in self.tabla

    def test_len(self):
        assert len(self.tabla) == 2

    def test_iter_claves(self):
        assert set(self.tabla) == {"EST001", "EST002"}

    def test_rehash_automatico(self):
        tabla = HashTable(capacidad=2)
        for i in range(10):
            est = Estudiante(f"EST{i:03d}", f"Estudiante {i}", "Programa", 1)
            tabla[est.id_estudiante] = est
        assert len(tabla) == 10
        for i in range(10):
            assert f"EST{i:03d}" in tabla

    def test_manejo_colisiones(self):
        tabla = HashTable(capacidad=2)
        for i in range(5):
            tabla[f"CLAVE_{i}"] = i
        for i in range(5):
            assert tabla[f"CLAVE_{i}"] == i

    def test_obtener_con_default(self):
        assert self.tabla.obtener("NOEXISTE", "DEFAULT") == "DEFAULT"

    def test_items_genera_pares(self):
        pares = dict(self.tabla.items())
        assert pares["EST001"] == self.est1


class TestPlanificador:
    def setup_method(self):
        self.planificador = PlanificadorKernel()

    def test_encolar_asigna_pid(self):
        tarea = Tarea("test", Prioridad.NORMAL)
        self.planificador.encolar(tarea)
        assert tarea.pid is not None

    def test_desencolar_orden_prioridad(self):
        self.planificador.encolar(Tarea("baja",    Prioridad.BAJA))
        self.planificador.encolar(Tarea("critica", Prioridad.CRITICA))
        self.planificador.encolar(Tarea("normal",  Prioridad.NORMAL))
        assert self.planificador.desencolar().prioridad == Prioridad.CRITICA

    def test_desencolar_cola_vacia_lanza_error(self):
        with pytest.raises(IndexError):
            self.planificador.desencolar()

    def test_fifo_en_misma_prioridad(self):
        t1 = Tarea("primera", Prioridad.NORMAL, timestamp=1000.0)
        t2 = Tarea("segunda", Prioridad.NORMAL, timestamp=2000.0)
        self.planificador.encolar(t2)
        self.planificador.encolar(t1)
        assert self.planificador.desencolar().nombre == "primera"

    def test_lt_operator(self):
        assert Tarea("alta", Prioridad.ALTA) < Tarea("baja", Prioridad.BAJA)

    def test_peek_no_extrae(self):
        self.planificador.encolar(Tarea("test", Prioridad.ALTA))
        self.planificador.peek()
        assert len(self.planificador) == 1

    def test_esta_vacia(self):
        assert self.planificador.esta_vacia()
        self.planificador.encolar(Tarea("t", Prioridad.NORMAL))
        assert not self.planificador.esta_vacia()

    def test_len(self):
        for i in range(5):
            self.planificador.encolar(Tarea(f"t{i}", Prioridad.NORMAL))
        assert len(self.planificador) == 5

    def test_ejecutar_todas_orden_correcto(self):
        for p in [Prioridad.BAJA, Prioridad.CRITICA, Prioridad.NORMAL, Prioridad.ALTA]:
            self.planificador.encolar(Tarea(p.name, p))
        valores = [t.prioridad for t in self.planificador.ejecutar_todas()]
        assert valores == sorted(valores)

    def test_cambiar_prioridad(self):
        self.planificador.encolar(Tarea("proceso", Prioridad.BAJA))
        self.planificador.encolar(Tarea("otro", Prioridad.ALTA))
        self.planificador.cambiar_prioridad("proceso", Prioridad.CRITICA)
        assert self.planificador.desencolar().nombre == "proceso"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
