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
/**
 * 
 * @export
 * @interface RequestPresentationAction
 */
export interface RequestPresentationAction {
    /**
     * The action to perform on the proof presentation record.
     * @type {string}
     * @memberof RequestPresentationAction
     */
    action: RequestPresentationActionActionEnum;
    /**
     * The unique identifier of the issue credential record - and hence VC - to use as the prover accepts the presentation request. Only applicable on the prover side when the action is `request-accept`.
     * @type {Array<string>}
     * @memberof RequestPresentationAction
     */
    proofId?: Array<string>;
}


/**
 * @export
 */
export const RequestPresentationActionActionEnum = {
    RequestAccept: 'request-accept',
    RequestReject: 'request-reject',
    PresentationAccept: 'presentation-accept',
    PresentationReject: 'presentation-reject'
} as const;
export type RequestPresentationActionActionEnum = typeof RequestPresentationActionActionEnum[keyof typeof RequestPresentationActionActionEnum];


/**
 * Check if a given object implements the RequestPresentationAction interface.
 */
export function instanceOfRequestPresentationAction(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "action" in value;

    return isInstance;
}

export function RequestPresentationActionFromJSON(json: any): RequestPresentationAction {
    return RequestPresentationActionFromJSONTyped(json, false);
}

export function RequestPresentationActionFromJSONTyped(json: any, ignoreDiscriminator: boolean): RequestPresentationAction {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'action': json['action'],
        'proofId': !exists(json, 'proofId') ? undefined : json['proofId'],
    };
}

export function RequestPresentationActionToJSON(value?: RequestPresentationAction | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'action': value.action,
        'proofId': value.proofId,
    };
}

