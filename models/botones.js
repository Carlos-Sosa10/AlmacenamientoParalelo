'use strict'

const mongoose = require('mongoose')
const Schema = mongoose.Schema

const botonesSchema = Schema({
    //name: String,
    //btnId: String,
    btn: String,
    pos: String,
    temp: String
})

module.exports = mongoose.model('botones', botonesSchema)
