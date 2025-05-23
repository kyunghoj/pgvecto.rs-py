# TODO: remove after Python < 3.9 is no longer used
from __future__ import annotations

from typing import Any, Literal, Optional, Union

import toml

QuantizationType = Literal["trivial", "scalar", "product"]
QuantizationRatio = Literal["x4", "x8", "x16", "x32", "x64"]


class Quantization:
    def __init__(
        self,
        typ: QuantizationType = "trivial",
        ratio: Optional[QuantizationRatio] = None,
    ) -> None:
        self.type = typ
        self.ratio = ratio

    def dump(self) -> dict:
        if self.type == "product":
            return {"quantization": {"product": {"ratio": self.ratio}}}
        elif self.type == "scalar":
            return {"quantization": {"scalar": {}}}
        else:
            return {}


class Flat:
    def __init__(self, quantization: Optional[Quantization] = None):
        self.quantization = quantization

    def dump(self) -> dict:
        child: dict[str, Any] = {}
        if self.quantization is not None:
            child.update(self.quantization.dump())
        return {"flat": child}


class Hnsw:
    def __init__(
        self,
        m: Optional[int] = None,
        ef_construction: Optional[int] = None,
        quantization: Optional[Quantization] = None,
    ):
        self.m = m
        self.ef_construction = ef_construction
        self.quantization = quantization

    def dump(self) -> dict:
        child: dict[str, Any] = {}
        if self.quantization is not None:
            child.update(self.quantization.dump())
        if self.m is not None:
            child.update({"m": self.m})
        if self.ef_construction is not None:
            child.update({"ef_construction": self.ef_construction})
        return {"hnsw": child}


class Ivf:
    def __init__(
        self, nlist: Optional[int] = None, quantization: Optional[Quantization] = None
    ):
        self.nlist = nlist
        self.quantization = quantization

    def dump(self) -> dict:
        child: dict[str, Any] = {}
        if self.quantization is not None:
            child.update(self.quantization.dump())
        if self.nlist is not None:
            child.update({"nlist": self.nlist})
        return {"ivf": child}


class Vamana:
    def __init__(
        self,
        alpha: Optional[float] = None, # 1.2
        r: Optional[int] = None, # node 하나당 최대 엣지 개수
        l_search: Optional[int] = None, # index 구축시 서치 깊이 (노드 몇 개): 클수록 정확도 높아지나 오래걸림
        quantization: Optional[Quantization] = None
    ):
        self.alpha = alpha
        self.r = r
        self.l_search = l_search
        self.quantization = quantization

    def dump(self) -> dict:
        child: dict[str, Any] = {}
        if self.quantization is not None:
            child.update(self.quantization.dump())
        if self.alpha is not None:
            child.update({"alpha": self.alpha})
        if self.r is not None:
            child.update({"r": self.r})
        if self.l_search is not None:
            child.update({"l_search": self.l_search})
        return {"vamana": child}

class IndexOption:
    def __init__(
        self,
        index: Union[Hnsw, Ivf, Flat, Vamana],
        threads: Optional[int] = None,
    ):
        self.index = index
        self.threads = threads

    def dump(self) -> dict:
        child: dict[str, Any] = {"indexing": self.index.dump()}
        if self.threads is not None:
            child["optimizing"] = {"optimizing_threads": self.threads}
        return child

    def dumps(self) -> str:
        return toml.dumps(self.dump())
