#![allow(dead_code)]
#![allow(unused_imports)]

use std::collections::HashMap;

struct Object<'a> {
    val: &'a str,
}

impl Object<'_> {
    fn from(v: &str) -> Object {
        Object { val: v }
    }
}

impl std::fmt::Debug for Object<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "<object:{}>", self.val)
    }
}

fn main() {
    env_logger::init();

    let hello = Object::from("Hello");
    log::debug!("{:?}", hello);
}
