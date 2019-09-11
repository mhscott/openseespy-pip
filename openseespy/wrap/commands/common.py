import openseespy.opensees as opy
from openseespy.wrap.base_models import OpenseesObject


def set_node_mass(node, x_mass, y_mass, rot_mass):
    opy.mass(node.tag, x_mass, y_mass, rot_mass)


class Mass(OpenseesObject):
    op_base_type = "mass"
    op_type = None

    def __init__(self, osi, node, x_mass, y_mass, rot_mass):
        self.node = node
        self.x_mass = x_mass
        self.y_mass = y_mass
        self.rot_mass = rot_mass
        self._parameters = [self.node.tag, self.x_mass, self.y_mass, self.rot_mass]
        self.to_process(osi)


def set_equal_dofs(node_1, node_2, dof):
    opy.equalDOF(node_1.tag, node_2.tag,  dof)


class EqualDOF(OpenseesObject):
    op_base_type = "equalDOF"
    op_type = None

    def __init__(self, osi, node_1, node_2, dofs):
        self.node_1 = node_1
        self.node_2 = node_2
        self.dofs = dofs
        self._parameters = [self.node_1.tag, self.node_2.tag, *self.dofs]
        self.to_process(osi)


def set_node_fixities(node, x, y, z_rot, z=None, x_rot=None, y_rot=None):

    opy.fix(node.tag, x, y, z_rot)  # TODO: is order correct? deal with 3D


class Fix(OpenseesObject):
    op_base_type = "fix"
    op_type = None

    def __init__(self, osi, node, x, y, z_rot, z=None, x_rot=None, y_rot=None):
        self.node = node
        self.x = x
        self.y = y
        self.z_rot = z_rot
        self._parameters = [self.node.tag, self.x, self.y, self.z_rot]
        self.to_process(osi)


def analyze(osi, num_inc=1, dt=0.1, dt_min=None, dt_max=None, jd=None):
    if dt_min is None:
        parameters = [int(num_inc), float(dt)]
    else:
        parameters = [int(num_inc), float(dt), dt_min, dt_max, jd]
    opy.analyze(*parameters)
    if osi.state in [1, 3]:
        para = []
        for i, e in enumerate(parameters):
            if isinstance(e, str):
                e = "'%s'" % e
            para.append(str(e))
            if i > 40:  # avoid verbose print output
                break
        p_str = ', '.join(para)
        osi.to_commands('opy.analyze(%s)' % p_str)
    return 0


def set_time(osi, time):
    osi.to_commands('opy.setTime(%s)' % str(time))


def wipe_analysis(osi):
    osi.to_commands('opy.wipeAnalysis')


def update_material_stage(osi, material, stage):
    osi.to_commands("opy.updateMaterialStage('-material', {0}, '-stage', {1})".format(material.tag, stage))