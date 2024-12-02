from OpenGL.GL import *
from Mesh import *
import pygame

class MeshPart:
    def __init__(self, vertices, tex_coords, normals, material=None):
        self.vertices = vertices
        self.tex_coords = tex_coords
        self.normals = normals
        self.material = material


class LoadMesh:
    def __init__(self, file_path, draw_mode):
        self.draw_mode = draw_mode
        self.parts = self.load_obj(file_path)

    def load_obj(self, file_path):
        vertices = []
        textures = []
        normals = []
        parts = []
        current_part = {'vertices': [], 'tex_coords': [], 'normals': [], 'material': None}

        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertices.append(tuple(map(float, line.strip().split()[1:])))
                elif line.startswith('vt '):
                    textures.append(tuple(map(float, line.strip().split()[1:])))
                elif line.startswith('vn '):
                    normals.append(tuple(map(float, line.strip().split()[1:])))
                elif line.startswith('f '):
                    face_vertices = line.strip().split()[1:]
                    for vertex in face_vertices:
                        vtn = vertex.split('/')
                        vi = int(vtn[0]) - 1 if vtn[0] else 0
                        ti = int(vtn[1]) - 1 if len(vtn) > 1 and vtn[1] else None
                        ni = int(vtn[2]) - 1 if len(vtn) > 2 and vtn[2] else None

                        current_part['vertices'].append(vertices[vi])

                        if ti is not None:
                            current_part['tex_coords'].append(textures[ti])
                        else:
                            current_part['tex_coords'].append((0, 0))  # valor padrão para texturas

                        if ni is not None:
                            current_part['normals'].append(normals[ni])
                        else:
                            current_part['normals'].append((0.0, 0.0, 0.0))  # valor padrão para normais

                    parts.append(MeshPart(**current_part))
                    current_part = {'vertices': [], 'tex_coords': [], 'normals': [], 'material': None}

        return parts
