console.log("cloudant tutorial..."); 
/**
 * Get all dealerships
 **/
const Cloudant = require('@cloudant/cloudant');
/* async function main(params) { */
 async function main() {  
     const cloudant = Cloudant({
         url: "https://19a9416e-75db-496f-9156-b7fcb658e1af-bluemix.cloudantnosqldb.appdomain.cloud",
         plugins: {
             iamauth: {
                 iamApiKey: "ryC7o8JymgX_u7rphRscO0AWUIOT3i93ohLKA4bfGonk"
             }
         }
         /*
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
         */
     });
 
     try {
         let dbList = await cloudant.db.list();
         return { "dbs": dbList };
     } catch (error) {
         return { error: error.description };
     }
 }
 