# pylint: skip-file
from flexstack.utils.asn1.etsi_its_cdd import ETSI_ITS_CDD_ASN1_DESCRIPTIONS

CAM_ASN1_DESCRIPTIONS = (
    ETSI_ITS_CDD_ASN1_DESCRIPTIONS
    + """
CAM-PDU-Descriptions  {itu-t (0) identified-organization (4) etsi (0) itsDomain (5) wg1 (1) camPduRelease2 (103900) major-version-2 (2) minor-version-1 (1)} 

DEFINITIONS AUTOMATIC TAGS ::=

BEGIN

IMPORTS 
ItsPduHeader, CauseCodeV2, ReferencePosition, AccelerationControl, Curvature, CurvatureCalculationMode, Heading, LanePosition, EmergencyPriority, EmbarkationStatus, Speed, 
DriveDirection, AccelerationComponent, StationType, ExteriorLights, DangerousGoodsBasic, SpecialTransportType, LightBarSirenInUse, 
VehicleRole, VehicleLength, VehicleWidth, Path, RoadworksSubCauseCode, ClosedLanes, TrafficRule, SpeedLimit, SteeringWheelAngle, PerformanceClass, YawRate, 
PtActivation, ProtectedCommunicationZonesRSU, CenDsrcTollingZone, GenerationDeltaTime, BasicContainer

FROM ETSI-ITS-CDD {itu-t (0) identified-organization (4) etsi (0) itsDomain (5) wg1 (1) 102894 cdd (2) major-version-4 (4) minor-version-2 (2)}
;


--	The root data frame for cooperative awareness messages

/** 
* This type represents the CAM PDU.
*
* It shall include the following componenets:
*
* @field header: the header of the CAM PDU.
*
* @field cam: the payload of the CAM PDU.
*/ 

CAM ::= SEQUENCE {
	header ItsPduHeader (WITH COMPONENTS {... , protocolVersion (2), messageId(cam)}),
	cam    CamPayload
}

/**
* This type represents the CAM payload. 
*
* It shall include the following components: 
*
* @field generationDeltaTime: Time corresponding to the time of the reference position in the CAM, considered as time of the CAM generation.
*
* @field camParameters: The sequence of CAM mandatory and optional container.
*
*/
CamPayload ::= SEQUENCE {
	generationDeltaTime GenerationDeltaTime,
	camParameters       CamParameters
}

/**
* @field basicContainer: the mandatory basic container of the CAM.
*
* @field highFrequencyContainer: the mandatory container represents the high frequency of the CAM.
* 
* @field lowFrequencyContainer: the optional conatainer represents the low frequency of the CAM.
*
* @field specialVehicleContainer: The special container of the CAM shall be present as defined in clause 6.1.2. 
* The content of the container shall be set according to the value of the vehicleRole component as specified in Table 5. 
*/
CamParameters ::= SEQUENCE {
	basicContainer           BasicContainer,
	highFrequencyContainer   HighFrequencyContainer,
	lowFrequencyContainer    LowFrequencyContainer OPTIONAL,
	specialVehicleContainer  SpecialVehicleContainer OPTIONAL,
	...
}

/**
* This type represents the high frequency container.
* 
* It shall include the following components: 
*
* @field basicVehicleContainerHighFrequency: The mandatory high frequency container of the CAM when the originating ITS-S is of the type vehicle ITS-S.
*
* @field rsuContainerHighFrequency: The mandatory high frequency container of CAM when the type of the originating ITS-S is RSU ITS-S.
*/
HighFrequencyContainer ::= CHOICE {
	basicVehicleContainerHighFrequency BasicVehicleContainerHighFrequency,
	rsuContainerHighFrequency          RSUContainerHighFrequency,
	...
}

/**
* This type represents the low frequency container.
* 
* It shall include the following components: 
*
* The low frequency container of the CAM when the originating ITS-S is of the type vehicle ITS-S. It shall be present as defined in clause 6.1.2.
*/
 LowFrequencyContainer ::= CHOICE {
  basicVehicleContainerLowFrequency BasicVehicleContainerLowFrequency (WITH COMPONENTS {..., pathHistory (SIZE (0..23))}),
	...
}

/**
* This type represent the Special Vehicle Container.
*
* It shall include the following components:
*
* @field publicTransportContainer: If the vehicleRole component is set to publicTransport(1) this container shall be present.
*
* @field specialTransportContainer: If the vehicleRole component is set to specialTransport(2) this container shall be present.
*
* @field dangerousGoodsContainer: If the vehicleRole component is set to dangerousGoods(3) this container shall be present.
*
* @field roadWorksContainerBasic: If the vehicleRole component is set to roadWork(4) this container shall be present. 
*
* @field rescueContainer: If the vehicleRole component is set to rescue(5) this container shall be present. 
*
* @field emergencyContainer: If the vehicleRole component is set to emergency(6) this container shall be present.
*
* @field safetyCarContainer: If the vehicleRole component is set to safetyCar(7) this container shall be present. 
*/
SpecialVehicleContainer ::= CHOICE {
	publicTransportContainer  PublicTransportContainer,
	specialTransportContainer SpecialTransportContainer,
	dangerousGoodsContainer   DangerousGoodsContainer,
	roadWorksContainerBasic   RoadWorksContainerBasic,
	rescueContainer           RescueContainer,
	emergencyContainer        EmergencyContainer,
	safetyCarContainer        SafetyCarContainer,
	...
}

/**
* This type contains detaild information of the Basic Vehicle Container High Frequency.
*
* It shall include the following components:
*
* @field heading: It represent the heading and heading accuracy of the vehicle movement of the originating ITS-S with regards to the true north. 
* The heading accuracy provided in the heading Confidence value shall provide the accuracy of the measured vehicle heading with a confidence level 
* of 95 %. Otherwise, the value of the headingConfidence shall be set to unavailable.
*
* @field speed: It represent driving speed and speed accuracy of the originating ITS-S. The speed accuracy provided in the speedConfidence shall 
* provide the accuracy of the speed value with a confidence level of 95 %. Otherwise, the speedConfidence shall be set to unavailable.
*
* @field driveDirection: This component represent the vehicle drive direction (forward or backward) of the originating ITS-S.
*
* @field vehicleLength: This component represent the vehicle length value and vehicle length confidence indication of the vehicle ITS-S that 
* originate the CAM. 
*
* @field vehicleWidth: This component represents the Vehicle Width of the vehicle ITS-S that originates the CAM excluding side mirrors and possible
* similar extensions.
*
* @field longitudinalAcceleration: It represent the vehicle Longitudinal Acceleration of the originating ITS-S in the centre of the mass of the 
* empty vehicle. It shall include the measured vehicle longitudinal acceleration and its accuracy value with the confidence level of 95 %. 
* Otherwise, the longitudinalAccelerationConfidence shall be set to unavailable. 
*
* @field curvature: this component reppresent the actual trajectory of the vehicle. 
*
* @field curvatureCalculationMode: It indicates whether vehicle yaw-rate is used in the calculation of the curvature of the vehicle ITS-S that
* originates the CAM.
*
* @field yawRate: It denotes the vehicle rotation around the centre of mass of the empty vehicle. The leading sign denotes the direction of 
* rotation. The value is negative if the motion is clockwise when viewing from the top.
* yawRateConfidence denotes the accuracy for the 95 % confidence level for the measured yawRateValue. Otherwise, the value of yawRateConfidence
* shall be set to unavailable.
*
* @field accelerationControl: an optional component which represents the current status of the vehcile mechnanisms controlling the longitudinal movement of the vehcile ITS-S
* (e.g. brake pedal,  gas pedal, etc. engaged) that originate the CAM.
*
* @field lanePosition: an optional component which represents the lanePosition of the referencePosition of a vehicle. This component shall be present if the data is 
* available at the originating ITS-S.
*
* @field steeringWheelAngle: an optional component which indicates the steering wheel angle and accuracy as measured at the vehicle ITS-S that originates the CAM.
*
* @field lateralAcceleration: an optional component which represents the vehicle lateral acceleration of the originating ITS-S in the centre of the mass of the empty vehicle. 
* It shall include the measured vehicle lateral acceleration and its accuracy value with the confidence level of 95%.
*
* @field verticalAcceleration: an optional component which indicates the originating ITS-S in the centre of the mass of the empty vehicle.
* 
* @field performanceClass: an optional component characterizes the maximum age of the CAM data elements with regard to the generation delta time.
*
* @field cenDsrcTollingZone: an optional component which represents the information about the position of a CEN DSRC Tolling Station operating in the 5,8 GHz frequency band.
*/
BasicVehicleContainerHighFrequency ::= SEQUENCE {
	heading Heading,
	speed Speed,
	driveDirection DriveDirection,
	vehicleLength VehicleLength,
	vehicleWidth VehicleWidth,
	longitudinalAcceleration AccelerationComponent,
	curvature Curvature,
	curvatureCalculationMode CurvatureCalculationMode,
	yawRate YawRate,
	accelerationControl AccelerationControl OPTIONAL,
	lanePosition LanePosition OPTIONAL,
	steeringWheelAngle SteeringWheelAngle OPTIONAL,
	lateralAcceleration AccelerationComponent OPTIONAL,
	verticalAcceleration AccelerationComponent OPTIONAL,
	performanceClass PerformanceClass OPTIONAL,
	cenDsrcTollingZone CenDsrcTollingZone OPTIONAL
}

/**
* This type contains detaild information of the Basic Vehicle Container Low Frequency.
*
* It shall include the following components:
*
* @field vehicleRole: represent the role of the vehicle ITS-S that originates the CAM. Only values 0 to 7 shall be used.
*
* @field exteriorLights: represent the status of the most important exterior lights switches of the vehicle ITS-S that originates the CAM.
*
* @field pathHistory: which represents the vehicle's recent movement over some past time and/or distance. It consists of a list of path points,
* each represented as DF PathPoint. The list of path points may consist of up to 23 elements. 
*/
BasicVehicleContainerLowFrequency  ::= SEQUENCE {
	vehicleRole VehicleRole,
	exteriorLights ExteriorLights,
	pathHistory Path
}

/**
* This type contains detaild information of the Public Transport Container.
*
* It shall include the following components:
*
* @field embarkationStatus: It indicates whether the passenger embarkation is currently ongoing. 
*
* @field ptActivation: an optional component used for controlling traffic lights, barriers, bollards, etc.
*/
PublicTransportContainer ::= SEQUENCE {
	embarkationStatus EmbarkationStatus,
	ptActivation PtActivation OPTIONAL
}

/**
* This type contains detaild information of the Special Transport Container.
*
* It shall include the following components:
*
* @field specialTransportType: which indicates whether the originating ITS-S is mounted on a special transport vehicle with heavy or oversized load
* or both. It shall be present if the data is available in originating ITS-S.
*
* @field lightBarSirenInUse: indicates whether light-bar or a siren is in use by the vehicle originating the CAM.
*/
SpecialTransportContainer ::= SEQUENCE {
	specialTransportType SpecialTransportType,
	lightBarSirenInUse LightBarSirenInUse
}

/**
* This type contains detaild information of the Dangerous Goods Container.
*
* It shall include the following components:
*
* @field dangerousGoodsBasic: identifies the type of the dangerous goods transported by the vehicle that originates the CAM. It shall be present if
* the data is available in the originating ITS S.
*/
 DangerousGoodsContainer ::= SEQUENCE {
  dangerousGoodsBasic DangerousGoodsBasic
 }
 
 /**
* This type contains detaild information of the Road Works Container Basic.
*
* It shall include the following components:
*
* @field roadworksSubCauseCode: The optional component, in case the originating ITS-S is mounted to a vehicle ITS-S participating to roadwork. It 
* provides information on the type of roadwork that it is currently undertaking. This component shall be present if the data is available in 
* originating ITS S.
*
* @field lightBarSirenInUse: it indicates whether light-bar or a siren is in use by the vehicle originating the CAM.
*
* @field closedLanes: an optional component which provides information about the opening/closure status of the lanes ahead. Lanes are counted from
* the outside boarder of the road. If a lane is closed to traffic, the corresponding bit shall be set to 1.
*/
 RoadWorksContainerBasic ::= SEQUENCE {
  roadworksSubCauseCode RoadworksSubCauseCode OPTIONAL,
  lightBarSirenInUse LightBarSirenInUse,
  closedLanes ClosedLanes OPTIONAL
 }

/**
* This type contains detaild information of the Rescue Container.
*
* It shall include the following components:
*
* @field lightBarSirenInUse: it indicates whether light-bar or a siren is in use by the vehicle originating the CAM.
*/
RescueContainer ::= SEQUENCE {
	lightBarSirenInUse LightBarSirenInUse
}

/**
* This type contains detaild information of the Emergency Container.
*
* It shall include the following components:
*
* @field lightBarSirenInUse: it indicates whether light-bar or a siren is in use by the vehicle originating the CAM.
*
* @field incidentIndication: the optional incident related to the roadworks to provide additional information of the roadworks zone.
*
* @field emergencyPriority: the optional component represent right of way indicator of the vehicle ITS-S that originates the CAM PDU.
*/
EmergencyContainer ::= SEQUENCE {
	lightBarSirenInUse LightBarSirenInUse,
	incidentIndication CauseCodeV2 OPTIONAL,
	emergencyPriority EmergencyPriority OPTIONAL
}

/**
* This type contains detaild information of the Safety Car Container.
*
* It shall include the following components:
*
* @field lightBarSirenInUse: it indicates whether light-bar or a siren is in use by the vehicle originating the CAM.
*
* @field incidentIndication: the optional incident related to the roadworks to provide additional information of the roadworks zone.
*
* @field trafficRule: an optional rule indicates whether vehicles are allowed to overtake a safety car that is originating this CAM.
*
* @field speedLimit: an optional speed indicates whether a speed limit is applied to vehicles following the safety car. 
*/
SafetyCarContainer ::= SEQUENCE {
	lightBarSirenInUse LightBarSirenInUse,
	incidentIndication CauseCodeV2 OPTIONAL,
	trafficRule TrafficRule OPTIONAL,
	speedLimit SpeedLimit OPTIONAL
}

/**
* This type contains detaild information of the RSU Container High Frequency.
*
* It shall include the following components:
*
* @field protectedCommunicationZonesRSU: an optional Information about position of a CEN DSRC Tolling Station operating in the 5,8 GHz frequency 
* band. If this information is provided by RSUs a receiving vehicle ITS-S is prepared to adopt mitigation techniques when being in the vicinity of
* CEN DSRC tolling stations. 

*/
RSUContainerHighFrequency ::= SEQUENCE {
	protectedCommunicationZonesRSU ProtectedCommunicationZonesRSU OPTIONAL,
	...
}

END
"""
)
