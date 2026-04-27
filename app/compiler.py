FastAPI
 0.1.0 
OAS 3.1
/openapi.json
default


POST
/upload_and_compile
Upload And Compile

Parameters
Cancel
Reset
No parameters

Request body

multipart/form-data
file *
string
Modeling Legal Arguments2.pdf
Execute
Clear
Responses
Curl

curl -X 'POST' \
  'https://lexcompiler-production.up.railway.app/upload_and_compile' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@Modeling Legal Arguments2.pdf;type=application/pdf'
Request URL
https://lexcompiler-production.up.railway.app/upload_and_compile
Server response
Code	Details
200	
Response body
Download
{
  "nodes": [
    {
      "id": "1",
      "label": "Theory of similarity networks is developed",
      "node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "type": "FactorNode",
      "level": "Factual",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "2",
      "label": "Construction of a global knowledge map from a similarity network is sound for strictly positive distributions",
      "node_id": "6f572a47-e76a-4f41-bc1f-601aa5d82762",
      "type": "ClaimNode",
      "level": "Legal",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "3",
      "label": "A low-order polynomial algorithm exists for testing the consistency of a similarity network",
      "node_id": "f0eca995-7a4d-4c42-a14c-508ebc282da0",
      "type": "ClaimNode",
      "level": "Legal",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "4",
      "label": "Construction of a global knowledge map from a similarity network is exhaustive",
      "node_id": "bdf50eec-318f-41d2-b135-2263a7bbbbb4",
      "type": "ClaimNode",
      "level": "Legal",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "5",
      "label": "Any global knowledge map constructed for a given hypothesis set must contain all relevant features",
      "node_id": "cf55c6e7-4b47-4786-980c-29e478029e96",
      "type": "ClaimNode",
      "level": "Legal",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "6",
      "label": "Lowercase letters represent uncertain variables or nodes in a graph",
      "node_id": "76880fb7-ce9a-42b3-9310-6d44a90fe820",
      "type": "FactorNode",
      "level": "Factual",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "7",
      "label": "Uppercase letters represent sets of uncertain variables or nodes in a graph",
      "node_id": "4504a568-e820-4708-8b2b-dbcb81ff2a3c",
      "type": "FactorNode",
      "level": "Factual",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "8",
      "label": "X\\Y is the set of variables in X that are not in Y",
      "node_id": "df09d40e-4759-443d-a85c-4aa427a704be",
      "type": "FactorNode",
      "level": "Factual",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    },
    {
      "id": "9",
      "label": "p(xi|Xj, ξ) denotes the probability of xi given Xj assessed by a person with background knowledge ξ",
      "node_id": "1b7e7304-b262-4c6c-a27b-9f5a5b4633c5",
      "type": "FactorNode",
      "level": "Factual",
      "polarity": "Neutral",
      "cpt_priors": {
        "state_true": 0.5,
        "state_false": 0.5
      }
    }
  ],
  "edges": [
    {
      "source": "1",
      "target": "2",
      "edge_id": "63f8451d-7d0d-4d91-9375-3ddaf2a2c5b2",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "6f572a47-e76a-4f41-bc1f-601aa5d82762",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "3",
      "edge_id": "7ac62162-d390-429f-9348-24542ae434e1",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "f0eca995-7a4d-4c42-a14c-508ebc282da0",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "4",
      "edge_id": "d464df16-5d8b-4177-abc9-f5aa28126f28",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "bdf50eec-318f-41d2-b135-2263a7bbbbb4",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "4",
      "target": "5",
      "edge_id": "305bd9d5-a804-4208-a645-b0db317af41f",
      "source_node_id": "bdf50eec-318f-41d2-b135-2263a7bbbbb4",
      "target_node_id": "cf55c6e7-4b47-4786-980c-29e478029e96",
      "relation_type": "ConditionalDependency",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "6",
      "edge_id": "b3aa98fb-cf9f-49ce-9d1e-6041bbf6b4b6",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "76880fb7-ce9a-42b3-9310-6d44a90fe820",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "7",
      "edge_id": "746cc014-77df-46ce-816a-544a129b3467",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "4504a568-e820-4708-8b2b-dbcb81ff2a3c",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "8",
      "edge_id": "349f3c8d-893e-499a-86ec-69ca67483512",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "df09d40e-4759-443d-a85c-4aa427a704be",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    },
    {
      "source": "1",
      "target": "9",
      "edge_id": "9f31191e-3c3e-47f1-b063-cd615f16ef0e",
      "source_node_id": "4e20b039-836b-486f-aca4-7dea29538b49",
      "target_node_id": "1b7e7304-b262-4c6c-a27b-9f5a5b4633c5",
      "relation_type": "BAF_Support",
      "logic_gate": "NoisyOR"
    }
  ]
}
Response headers
 content-length: 4287 
 content-type: application/json 
 date: Mon,27 Apr 2026 08:40:03 GMT 
 server: railway-edge 
 x-cache: MISS 
 x-cache-hits: 0 
 x-railway-cdn-edge: fastly/cache-jax2030021-JAX 
 x-railway-edge: railway/us-east4-eqdc4a 
 x-railway-request-id: 2DobIDKoR4iLB4UWPvyhXg 
 x-served-by: cache-jax2030021-JAX 
Responses
Code	Description	Links
200	
Successful Response

Media type

application/json
Controls Accept header.
Example Value
Schema
"string"
No links
422	
Validation Error

Media type

application/json
Example Value
Schema
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string",
      "input": "string",
      "ctx": {}
    }
  ]
}
No links

POST
/run_inference
Inference


Schemas
Body_upload_and_compile_upload_and_compile_postExpand allobject
HTTPValidationErrorExpand allobject
ValidationErrorExpand allobject