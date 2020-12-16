//buenas practicas de .js
'use strict'

//importacion de express
const express = require('express')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const MiniP = require ('./models/botones.js')
const app = express()
const port = process.env.PORT || 3018
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())

app.get('/Minip/api',(req, res) => {
    //res.send({ message: 'Inicio Get' })

   MiniP.find({}, (err, mps) => {
        if(err) return res.status(500).send({message: `Request Error:${err}`})
        if(!mps) return res.status(404).send({message:`No hay valores`})

        res.send(200, { mps })
    })
})
app.get('/Minip/api/:botonID',(req, res) =>{
    let botonID = req.params.botonID

    MiniP.findById(botonID, (err,minip) => {
        if(err) return res.status(500).send({message: `Request Error:${err}`})
        if(!minip) return res.status(404).send({message:`No hay valores`})

        res.status(200).send({ minip })
    })
})

app.post('/Minip/api',(req, res) =>{
    //res.send({ message: 'Inicio Post' })

    console.log('POST /Minip/api')
    console.log(req.body)

    let Minip = new MiniP()
 
    Minip.btn = req.body.btn
    Minip.pos = req.body.pos
    Minip.date =req.body.date
    Minip.temp =req.body.temp
    
    Minip.save((err, MinipStored) =>{
      if (err) res.status(500).send({message: `Request Error BD:${err}` })
    
      res.status(200).send({Minip: MinipStored})
       })
})

app.put('/Minip/api/:botonID',(req, res) => {
   
})

app.delete('/Minip/api/:botonID',(req, res) =>{
    let botonID = req.params.botonID

    MiniP.findById(botonID, (err,minip) => {
        if(err) res.status(500).send({message: `Request Error:${err}`})
    

       minip.remove(err => {
        if (err) res.status(500).send({message: `Request Error: ${err}` })
        res.status(200).send({message: 'Se borro correctamente'})
       }) 
   })
})
mongoose.connect('mongodb://localhost:27017/minip',(err,res) => {
    if (err) {
        return console.log('Error al conectar la base de datos...')
    }
    if (err) throw err
    console.log('Conexión a la base de datos establecida')

    app.listen(port,() => {
        console.log(`API Mini Proyecto corriendo http://localhost:${port}`)
    })
})
