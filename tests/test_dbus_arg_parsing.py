#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from unittest import TestCase

from pystemd.dbuslib import (
    compile_args,
    compile_array,
    compile_simple,
    compile_struct,
    find_closure,
)


class TestCompileSimple(TestCase):
    def test_compile(self):
        signature = b"s"

        off, _ = compile_simple(signature)
        self.assertEqual(signature, off)

    def test_result_of_compile(self):
        signature = b"s"
        call_arg = b"arg"

        _, func = compile_simple(signature)

        self.assertEqual(func(call_arg), [(ord(signature), call_arg)])


class TestCompileArray(TestCase):
    def test_compile_array_with_simple_arg(self):
        signature = b"as"
        call_arg = [b"arg_1", b"arg_2"]

        off, func = compile_array(signature)

        self.assertEqual(signature, off)
        self.assertEqual(
            func(call_arg),
            [
                (ord(b"a"), signature[1:]),
                (ord(b"s"), b"arg_1"),
                (ord(b"s"), b"arg_2"),
                (-1, None),
            ],
        )

    def test_compile_double_array(self):
        signature = b"aas"
        call_arg = [[b"arg_1", b"arg_2"], [b"arg_a", b"arg_b"]]

        off, func = compile_array(signature)

        self.assertEqual(signature, off)
        self.assertEqual(
            func(call_arg),
            [
                (ord(b"a"), signature[1:]),
                (ord(b"a"), b"s"),
                (ord(b"s"), b"arg_1"),
                (ord(b"s"), b"arg_2"),
                (-1, None),
                (ord(b"a"), b"s"),
                (ord(b"s"), b"arg_a"),
                (ord(b"s"), b"arg_b"),
                (-1, None),
                (-1, None),
            ],
        )

    def test_compile_array_of_structs(self):
        signature = b"a(ss)"
        call_arg = [(b"arg_1", b"arg_2"), (b"arg_a", b"arg_b")]

        off, func = compile_array(signature)

        self.assertEqual(signature, off)
        self.assertEqual(
            func(call_arg),
            [
                (ord(b"a"), signature[1:]),
                (ord(b"r"), b"ss"),
                (ord(b"s"), b"arg_1"),
                (ord(b"s"), b"arg_2"),
                (-1, None),
                (ord(b"r"), b"ss"),
                (ord(b"s"), b"arg_a"),
                (ord(b"s"), b"arg_b"),
                (-1, None),
                (-1, None),
            ],
        )


class TestCompileStruct(TestCase):
    def test_compile(self):
        signature = b"(ss)"
        off, _ = compile_struct(signature)
        self.assertEqual(signature, off)

    def test_apply(self):
        signature = b"(ss)"
        call_arg = (b"arg_1", b"arg_2")

        _, func = compile_struct(signature)

        self.assertEqual(
            func(call_arg),
            [
                (ord(b"r"), signature[1:-1]),
                (ord(b"s"), b"arg_1"),
                (ord(b"s"), b"arg_2"),
                (-1, None),
            ],
        )


class TestCompileMainFunc(TestCase):
    def test_compile_array(self):
        signature = b"as"
        funcs = compile_args(signature)
        self.assertEqual(len(funcs), 1)

    def test_compile_simplest(self):
        signature = b"ssibb"
        funcs = compile_args(signature)
        self.assertEqual(len(funcs), len(signature))

    def test_compile_little_complex_expr(self):
        signature = b"s(si)abb"
        funcs = compile_args(signature)
        self.assertEqual(len(funcs), 4)
        self.assertEqual(
            [f.__name__ for f in funcs],
            ["process_simple", "process_struct", "process_array", "process_simple"],
        )


class TestFindClosure(TestCase):
    def test_closure(self):
        self.assertEqual(find_closure(b"(ss)", ord("("), ord(")")), 3)

    def test_multi_closure(self):
        self.assertEqual(find_closure(b"(s(s)aa(((s)))u)sss", ord("("), ord(")")), 15)
