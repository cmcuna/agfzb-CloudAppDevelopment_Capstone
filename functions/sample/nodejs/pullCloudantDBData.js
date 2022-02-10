console.log("cloudant tutorial...")
/* import our cloudant package */
const Cloudant = require('@cloudant/cloudant')
cloudant();

/* make the connection using async function */
async function cloudant(){
    try{
        console.log("creating cloudant conn...")
        /* create constant w/ instance of cloudant (pass in credentials) */
        const cloudant = Cloudant({
            url: "https://19a9416e-75db-496f-9156-b7fcb658e1af-bluemix.cloudantnosqldb.appdomain.cloud",
            plugins:{
                /* authentication with I AM */
                iamauth:{
                    iamApiKey: "ryC7o8JymgX_u7rphRscO0AWUIOT3i93ohLKA4bfGonk"
                }
            }
        })
        console.log("successfully created cloudant conn")

        /* let's get all databases by calling cloudant object*/
        console.log("getting cloudant databases...")
        let allDB = await cloudant.db.list()
        console.log("cloudant databases:", allDB)

        /* set database we will be using*/
        console.log("setting the database we are going to use...")
        const db = cloudant.db.use('reviews')
        console.log("using database:", db.config.db)

        let res=""

        /* get data from database*/
        console.log("get data from database...")
        res = await db.list({include_docs:true})
        console.log(res)

    }catch(error){
        console.error('Error:', error);
    }
}
