/* tslint:disable */
/* eslint-disable */
/**
 * Prism Agent
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { Json } from './Json';
import {
    JsonFromJSON,
    JsonFromJSONTyped,
    JsonToJSON,
} from './Json';
import type { ServiceType } from './ServiceType';
import {
    ServiceTypeFromJSON,
    ServiceTypeFromJSONTyped,
    ServiceTypeToJSON,
} from './ServiceType';

/**
 * A service expressed in the DID document. https://www.w3.org/TR/did-core/#services
 * @export
 * @interface Service
 */
export interface Service {
    /**
     * The id of the service.
     * Requires a URI fragment when use in create / update DID.
     * Returns the full ID (with DID prefix) when resolving DID
     * @type {string}
     * @memberof Service
     */
    id: string;
    /**
     * 
     * @type {ServiceType}
     * @memberof Service
     */
    type: ServiceType;
    /**
     * 
     * @type {Json}
     * @memberof Service
     */
    serviceEndpoint: Json;
}

/**
 * Check if a given object implements the Service interface.
 */
export function instanceOfService(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "type" in value;
    isInstance = isInstance && "serviceEndpoint" in value;

    return isInstance;
}

export function ServiceFromJSON(json: any): Service {
    return ServiceFromJSONTyped(json, false);
}

export function ServiceFromJSONTyped(json: any, ignoreDiscriminator: boolean): Service {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'type': ServiceTypeFromJSON(json['type']),
        'serviceEndpoint': JsonFromJSON(json['serviceEndpoint']),
    };
}

export function ServiceToJSON(value?: Service | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'type': ServiceTypeToJSON(value.type),
        'serviceEndpoint': JsonToJSON(value.serviceEndpoint),
    };
}

