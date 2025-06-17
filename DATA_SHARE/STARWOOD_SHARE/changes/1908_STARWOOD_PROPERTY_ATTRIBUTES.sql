--liquibase formatted sql

--changeset kusumasri.muddasani@invitationhomes.com:1908_STARWOOD_PROPERTY_ATTRIBUTES_v1.sql

create or replace secure view STARWOOD_PROPERTY_ATTRIBUTES(
	YARDIPROPERTYCODENEWCO,
	STREETADDRESSL1,
	CITY,
	STATE,
	ZIPCODE,
	ACTUALBLDGSQFT,
	YEARBUILT,
	REPORTINGMARKET,
	ASSETMGMTSUBMARKET,
	FUND,
	ACQUISITIONSTATUSCURRENT,
	LOCATION_LATITUDE,
	LOCATION_LONGITUDE,
	CURRENTLEASECATEGORY,
	COMMUNITYID,
	YARDIHOUSEHOLDCODE,
	HOUSEHOLDSTATUS,
	MOVEINDATE,
	MOVEOUTDATE,
	SSTATUS,
	LEASERESOLUTION,
	LEASETYPE,
	LEASECATEGORY,
	LEASETERMORIGINAL,
	LEASETERMMONTHS,
	EFFECTIVERENT,
	EFFECTIVERENTPRECEDING,
	LEASEBEGINDATEKEY,
	LEASECAPTUREDATE,
	LEASEENDACTUALDATEKEY,
	APPLICATIONDATE,
	NOTICEDATE
) as (
	WITH property_details AS (
    SELECT 
        yardipropertycodenewco,
        streetaddressl1,
        city,
        state,
        zipcode,
        actualbldgsqft,
        actuallotsqft,
        yearbuilt,
        reportingmarket,
        assetmgmtsubmarket,
        fund,
        acquisitionstatuscurrent,
        location_latitude,
        location_longitude,
        currentleasecategory,
        communityid
    FROM ${envId}_tz.edw.vwopsproduct
    WHERE portfoliogroup = 'Starwood'
	),

	household_status AS (
		SELECT 
			yardihouseholdcode,
			TRIM(LOWER(yardipropertycodenewco)) AS yardipropertycodenewco_clean,
			householdstatus,
			moveindate,
			currentaddressmoveoutdate AS moveoutdate
		FROM ${envId}_tz.edw.vwopscustomer
		WHERE householdstatus IN ('current', 'eviction', 'notice') 
		AND yardipropertycodenewco ILIKE '%sw%'
	),

	unit_rent_status AS (
		SELECT 
			TRIM(LOWER(scode)) AS scode_clean,
			srent,
			sstatus
		FROM ${envId}_rz.yardi_dbo.unit
	),

	lease_details AS (
		SELECT 
			yardihouseholdcode,
			TRIM(LOWER(yardipropertycodenewco)) AS yardipropertycodenewco_clean,
			leaseresolution,
			leasetype,
			leasecategory,
			leasetermoriginal,
			leasetermmonths,
			effectiverent,
			effectiverentpreceding,
			leasebegindatekey,
			leasecapturedate,
			leaseendactualdatekey,
			applicationdate,
			noticedate
		FROM ${envId}_tz.edw.vwopslease
		WHERE yardipropertycodenewco ILIKE '%sw%' 
		AND leasestatus = 'Active'
	)

	SELECT 
		-- Property Details columns
		pd.yardipropertycodenewco,
		pd.streetaddressl1,
		pd.city,
		pd.state,
		pd.zipcode,
		pd.actualbldgsqft,
		pd.yearbuilt,
		pd.reportingmarket,
		pd.assetmgmtsubmarket,
		pd.fund,
		pd.acquisitionstatuscurrent,
		pd.location_latitude,
		pd.location_longitude,
		pd.currentleasecategory,
		pd.communityid,

		-- Household Status columns
		hs.yardihouseholdcode,
		hs.householdstatus,
		hs.moveindate,
		hs.moveoutdate,

		-- Unit Rent Status column
		urs.sstatus,
		
		-- Lease Details columns
		ld.leaseresolution,
		ld.leasetype,
		ld.leasecategory,
		ld.leasetermoriginal,
		ld.leasetermmonths,
		ld.effectiverent,
		ld.effectiverentpreceding,
		ld.leasebegindatekey,
		ld.leasecapturedate,
		ld.leaseendactualdatekey,
		ld.applicationdate,
		ld.noticedate

	FROM property_details pd
	LEFT JOIN household_status hs 
		ON TRIM(LOWER(pd.yardipropertycodenewco)) = hs.yardipropertycodenewco_clean
	LEFT JOIN unit_rent_status urs 
		ON TRIM(LOWER(pd.yardipropertycodenewco)) = urs.scode_clean
	LEFT JOIN lease_details ld 
		ON TRIM(LOWER(pd.yardipropertycodenewco)) = ld.yardipropertycodenewco_clean
);