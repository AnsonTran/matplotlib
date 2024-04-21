from .path import Path
from .patches import Patch
from .figure import Figure
import numpy as np
from numpy.typing import ArrayLike
from collections.abc import Iterable, Sequence
from typing import Literal

DEBUG: bool

class TransformNode:
    INVALID_NON_AFFINE: int
    INVALID_AFFINE: int
    INVALID: int
    is_bbox: bool
    # Implemented as a standard attr in base class, but functionally readonly and some subclasses implement as such
    @property
    def is_affine(self) -> bool: ...
    pass_through: bool
    def __init__(self, shorthand_name: str | None = ...) -> None: ...
    def __copy__(self) -> TransformNode: ...
    def invalidate(self) -> None: ...
    def set_children(self, *children: TransformNode) -> None: ...
    def frozen(self) -> TransformNode: ...

class BboxBase(TransformNode):
    is_bbox: bool
    is_affine: bool
    def frozen(self) -> Bbox: ...
    def __array__(self, *args, **kwargs): ...
    @property
    def x0(self) -> float: ...
    @property
    def y0(self) -> float: ...
    @property
    def x1(self) -> float: ...
    @property
    def y1(self) -> float: ...
    @property
    def p0(self) -> tuple[float, float]: ...
    @property
    def p1(self) -> tuple[float, float]: ...
    @property
    def xmin(self) -> float: ...
    @property
    def ymin(self) -> float: ...
    @property
    def xmax(self) -> float: ...
    @property
    def ymax(self) -> float: ...
    @property
    def min(self) -> tuple[float, float]: ...
    @property
    def max(self) -> tuple[float, float]: ...
    @property
    def intervalx(self) -> tuple[float, float]: ...
    @property
    def intervaly(self) -> tuple[float, float]: ...
    @property
    def width(self) -> float: ...
    @property
    def height(self) -> float: ...
    @property
    def size(self) -> tuple[float, float]: ...
    @property
    def bounds(self) -> tuple[float, float, float, float]: ...
    @property
    def extents(self) -> tuple[float, float, float, float]: ...
    def get_points(self) -> np.ndarray: ...
    def containsx(self, x: float) -> bool: ...
    def containsy(self, y: float) -> bool: ...
    def contains(self, x: float, y: float) -> bool: ...
    def overlaps(self, other: BboxBase) -> bool: ...
    def fully_containsx(self, x: float) -> bool: ...
    def fully_containsy(self, y: float) -> bool: ...
    def fully_contains(self, x: float, y: float) -> bool: ...
    def fully_overlaps(self, other: BboxBase) -> bool: ...
    def transformed(self, transform: Transform) -> Bbox: ...
    coefs: dict[str, tuple[float, float]]
    # anchored type can be s/str/Literal["C", "SW", "S", "SE", "E", "NE", "N", "NW", "W"]
    def anchored(
        self, c: tuple[float, float] | str, container: BboxBase | None = ...
    ) -> Bbox: ...
    def shrunk(self, mx: float, my: float) -> Bbox: ...
    def shrunk_to_aspect(
        self,
        box_aspect: float,
        container: BboxBase | None = ...,
        fig_aspect: float = ...,
    ) -> Bbox: ...
    def splitx(self, *args: float) -> list[Bbox]: ...
    def splity(self, *args: float) -> list[Bbox]: ...
    def count_contains(self, vertices: ArrayLike) -> int: ...
    def count_overlaps(self, bboxes: Iterable[BboxBase]) -> int: ...
    def expanded(self, sw: float, sh: float) -> Bbox: ...
    def padded(self, w_pad: float, h_pad: float | None = ...) -> Bbox: ...
    def translated(self, tx: float, ty: float) -> Bbox: ...
    def corners(self) -> np.ndarray: ...
    def rotated(self, radians: float) -> Bbox: ...
    @staticmethod
    def union(bboxes: Sequence[BboxBase]) -> Bbox: ...
    @staticmethod
    def intersection(bbox1: BboxBase, bbox2: BboxBase) -> Bbox | None: ...

class Bbox(BboxBase):
    def __init__(self, points: ArrayLike, **kwargs) -> None: ...
    @staticmethod
    def unit() -> Bbox: ...
    @staticmethod
    def null() -> Bbox: ...
    @staticmethod
    def from_bounds(x0: float, y0: float, width: float, height: float) -> Bbox: ...
    @staticmethod
    def from_extents(*args: float, minpos: float | None = ...) -> Bbox: ...
    def __format__(self, fmt: str) -> str: ...
    def ignore(self, value: bool) -> None: ...
    def update_from_path(
        self,
        path: Path,
        ignore: bool | None = ...,
        updatex: bool = ...,
        updatey: bool = ...,
    ) -> None: ...
    def update_from_data_x(self, x: ArrayLike, ignore: bool | None = ...) -> None: ...
    def update_from_data_y(self, y: ArrayLike, ignore: bool | None = ...) -> None: ...
    def update_from_data_xy(
        self,
        xy: ArrayLike,
        ignore: bool | None = ...,
        updatex: bool = ...,
        updatey: bool = ...,
    ) -> None: ...
    @property
    def minpos(self) -> float: ...
    @property
    def minposx(self) -> float: ...
    @property
    def minposy(self) -> float: ...
    def get_points(self) -> np.ndarray: ...
    def set_points(self, points: ArrayLike) -> None: ...
    def set(self, other: Bbox) -> None: ...
    def mutated(self) -> bool: ...
    def mutatedx(self) -> bool: ...
    def mutatedy(self) -> bool: ...

class TransformedBbox(BboxBase):
    def __init__(self, bbox: Bbox, transform: Transform, **kwargs) -> None: ...
    def get_points(self) -> np.ndarray: ...

class LockableBbox(BboxBase):
    def __init__(
        self,
        bbox: BboxBase,
        x0: float | None = ...,
        y0: float | None = ...,
        x1: float | None = ...,
        y1: float | None = ...,
        **kwargs
    ) -> None: ...
    @property
    def locked_x0(self) -> float | None: ...
    @locked_x0.setter
    def locked_x0(self, x0: float | None) -> None: ...
    @property
    def locked_y0(self) -> float | None: ...
    @locked_y0.setter
    def locked_y0(self, y0: float | None) -> None: ...
    @property
    def locked_x1(self) -> float | None: ...
    @locked_x1.setter
    def locked_x1(self, x1: float | None) -> None: ...
    @property
    def locked_y1(self) -> float | None: ...
    @locked_y1.setter
    def locked_y1(self, y1: float | None) -> None: ...

class Transform(TransformNode):

    # Implemented as a standard attrs in base class, but functionally readonly and some subclasses implement as such
    @property
    def input_dims(self) -> int | None: ...
    @property
    def output_dims(self) -> int | None: ...
    @property
    def is_separable(self) -> bool: ...
    @property
    def has_inverse(self) -> bool: ...

    def __add__(self, other: Transform) -> Transform: ...
    @property
    def depth(self) -> int: ...
    def contains_branch(self, other: Transform) -> bool: ...
    def contains_branch_seperately(
        self, other_transform: Transform
    ) -> Sequence[bool]: ...
    def __sub__(self, other: Transform) -> Transform: ...
    def __array__(self, *args, **kwargs) -> np.ndarray: ...
    def transform(self, values: ArrayLike) -> np.ndarray: ...
    def transform_affine(self, values: ArrayLike) -> np.ndarray: ...
    def transform_non_affine(self, values: ArrayLike) -> ArrayLike: ...
    def transform_bbox(self, bbox: BboxBase) -> Bbox: ...
    def get_affine(self) -> Transform: ...
    def get_matrix(self) -> np.ndarray: ...
    def transform_point(self, point: ArrayLike) -> np.ndarray: ...
    def transform_path(self, path: Path) -> Path: ...
    def transform_path_affine(self, path: Path) -> Path: ...
    def transform_path_non_affine(self, path: Path) -> Path: ...
    def transform_angles(
        self,
        angles: ArrayLike,
        pts: ArrayLike,
        radians: bool = ...,
        pushoff: float = ...,
    ) -> np.ndarray: ...
    def inverted(self) -> Transform: ...

class TransformWrapper(Transform):
    pass_through: bool
    def __init__(self, child: Transform) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def frozen(self) -> Transform: ...
    def set(self, child: Transform) -> None: ...

class AffineBase(Transform):
    is_affine: Literal[True]
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class AffineImmutable(AffineBase):
    def __init__(self, *args, dims: int = ..., **kwargs) -> None: ...
    def frozen(self) -> AffineImmutable: ...
    def to_values(self) -> tuple[float]: ...

class Affine2DBase(AffineImmutable):
    pass

class Affine2D(AffineImmutable):
    def __init__(self, matrix: ArrayLike | None = ..., **kwargs) -> None: ...
    @staticmethod
    def from_values(
        a: float, b: float, c: float, d: float, e: float, f: float
    ) -> Affine2D: ...
    def set_matrix(self, mtx: ArrayLike) -> None: ...
    def clear(self) -> Affine2D: ...
    def rotate(self, theta: float) -> Affine2D: ...
    def rotate_deg(self, degrees: float) -> Affine2D: ...
    def rotate_around(self, x: float, y: float, theta: float) -> Affine2D: ...
    def rotate_deg_around(self, x: float, y: float, degrees: float) -> Affine2D: ...
    def translate(self, tx: float, ty: float) -> Affine2D: ...
    def scale(self, sx: float, sy: float | None = ...) -> Affine2D: ...
    def skew(self, xShear: float, yShear: float) -> Affine2D: ...
    def skew_deg(self, xShear: float, yShear: float) -> Affine2D: ...

class IdentityTransform(AffineImmutable): ...

class _BlendedMixin:
    def __eq__(self, other: object) -> bool: ...
    def contains_branch_seperately(self, transform: Transform) -> Sequence[bool]: ...

class BlendedGenericTransform(_BlendedMixin, Transform):
    input_dims: Literal[2]
    output_dims: Literal[2]
    pass_through: bool
    def __init__(
        self, x_transform: Transform, y_transform: Transform, **kwargs
    ) -> None: ...
    @property
    def depth(self) -> int: ...
    def contains_branch(self, other: Transform) -> Literal[False]: ...
    @property
    def is_affine(self) -> bool: ...

class BlendedAffine2D(_BlendedMixin, Affine2DBase):
    def __init__(
        self, x_transform: Transform, y_transform: Transform, **kwargs
    ) -> None: ...

def blended_transform_factory(
    x_transform: Transform, y_transform: Transform
) -> BlendedGenericTransform | BlendedAffine2D: ...

class CompositeGenericTransform(Transform):
    pass_through: bool
    def __init__(self, a: Transform, b: Transform, **kwargs) -> None: ...

class CompositeAffine2D(Affine2DBase):
    def __init__(self, a: Affine2DBase, b: Affine2DBase, **kwargs) -> None: ...
    @property
    def depth(self) -> int: ...

def composite_transform_factory(a: Transform, b: Transform) -> Transform: ...

class BboxTransform(AffineImmutable):
    def __init__(self, boxin: BboxBase, boxout: BboxBase, **kwargs) -> None: ...

class BboxTransformTo(AffineImmutable):
    def __init__(self, boxout: BboxBase, **kwargs) -> None: ...

class BboxTransformToMaxOnly(BboxTransformTo): ...

class BboxTransformFrom(AffineImmutable):
    def __init__(self, boxin: BboxBase, **kwargs) -> None: ...

class ScaledTranslation(AffineImmutable):
    def __init__(
        self, xt: float, yt: float, scale_trans: AffineImmutable, **kwargs
    ) -> None: ...

class AffineDeltaTransform(AffineImmutable):
    def __init__(self, transform: AffineImmutable, **kwargs) -> None: ...

class TransformedPath(TransformNode):
    def __init__(self, path: Path, transform: Transform) -> None: ...
    def get_transformed_points_and_affine(self) -> tuple[Path, Transform]: ...
    def get_transformed_path_and_affine(self) -> tuple[Path, Transform]: ...
    def get_fully_transformed_path(self) -> Path: ...
    def get_affine(self) -> Transform: ...

class TransformedPatchPath(TransformedPath):
    def __init__(self, patch: Patch) -> None: ...

def nonsingular(
    vmin: float,
    vmax: float,
    expander: float = ...,
    tiny: float = ...,
    increasing: bool = ...,
) -> tuple[float, float]: ...
def interval_contains(interval: tuple[float, float], val: float) -> bool: ...
def interval_contains_open(interval: tuple[float, float], val: float) -> bool: ...
def offset_copy(
    trans: Transform,
    fig: Figure | None = ...,
    x: float = ...,
    y: float = ...,
    units: Literal["inches", "points", "dots"] = ...,
) -> Transform: ...
