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

        let res="newdatabase"

        /* let's create a database */
        // console.log("creating cloudant database...")
        // const db = await cloudant.db.create(res)

        /* let's delete a database */
        console.log("deleting cloudant database...")
        await cloudant.db.destroy(res)

        /* let's get all databases by calling cloudant object */
        console.log("getting cloudant databases...")
        let allDB = await cloudant.db.list()
        console.log("cloudant databases:", allDB)

    }catch(error){
        console.error('Error:', error);
    }
}
