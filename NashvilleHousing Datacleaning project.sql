/*

 Cleaning Data in SQl Query

*/

select * from [PortfolioProject ]..NashvilleHousing

---------------------------------------------------------------------------------------------------------------------------

--Standardize Date Format

select saleDate,Convert(date,saledate)
from [PortfolioProject ]..NashvilleHousing

Alter table portfolioProject..NashvilleHousing 
Add saledateConverted date;

Update portfolioproject..NashvilleHousing
set saledateConverted = Convert(date,saledate)


------------------------------------------------------------------------------------------------------------------------------------

--Populate Property Address



select a.parcelid ,a.propertyaddress,b.parcelid,b.propertyaddress , isNull(a.propertyaddress,b.propertyaddress)
from 
[PortfolioProject ]..NashvilleHousing a join
[PortfolioProject ]..NashvilleHousing b
on a.parcelid = b.parcelid and
a.uniqueid <> b.uniqueid
where a.propertyaddress is null



update a
set PropertyAddress = isNull(a.propertyaddress,b.propertyaddress)
from 
[PortfolioProject ]..NashvilleHousing a join
[PortfolioProject ]..NashvilleHousing b
on a.parcelid = b.parcelid and
a.uniqueid <> b.uniqueid
where a.propertyaddress is null


-----------------------------------------------------------------------------------------------------------------------------------------
--Breakingout Address into individual column(Address,City,State)

select propertyaddress from [PortfolioProject ]..NashvilleHousing

select
substring(propertyaddress,1,CHARINDEX(',',propertyaddress)-1) as Address,
substring(propertyaddress,CHARINDEX(',',propertyaddress)+1,Len(propertyAddress)) as Address

from [PortfolioProject ]..NashvilleHousing

Alter table portfolioProject..NashvilleHousing 
Add PropertSplitAddress Nvarchar(255);

Update portfolioproject..NashvilleHousing
set PropertSplitAddress = substring(propertyaddress,1,CHARINDEX(',',propertyaddress)-1)

Alter table portfolioProject..NashvilleHousing 
Add PropeertySplitCity Nvarchar(255);

Update portfolioproject..NashvilleHousing
set PropeertySplitCity = substring(propertyaddress,CHARINDEX(',',propertyaddress)+1,Len(propertyAddress))

select * from [PortfolioProject ]..NashvilleHousing



select owneraddress from [PortfolioProject ]..NashvilleHousing

select
parsename(Replace(owneraddress,',','.'),3),
parsename(Replace(owneraddress,',','.'),2),
parsename(Replace(owneraddress,',','.'),1)
from [PortfolioProject ]..NashvilleHousing

Alter table portfolioProject..NashvilleHousing 
Add OwnerSplitAddress Nvarchar(255);

Update portfolioproject..NashvilleHousing
set OwnerSplitAddress = parsename(Replace(owneraddress,',','.'),3)

Alter table portfolioProject..NashvilleHousing 
Add OwnerSplitCity Nvarchar(255);

Update portfolioproject..NashvilleHousing
set OwnerSplitCity = parsename(Replace(owneraddress,',','.'),2)

Alter table portfolioProject..NashvilleHousing 
Add OwnerSplitState Nvarchar(255);

Update portfolioproject..NashvilleHousing
set OwnerSplitState = parsename(Replace(owneraddress,',','.'),1)

select * from [PortfolioProject ]..NashvilleHousing


---------------------------------------------------------------------------------------------------------------------------------

--Change Y and N into Yes and No in "sold as vacant" column

select distinct(soldasvacant),count(soldasvacant)
from [PortfolioProject ]..NashvilleHousing
group by soldasvacant
order by 2

update [PortfolioProject ]..NashvilleHousing
set soldasvacant = case when soldasvacant = 'Y' then 'Yes'
						when soldasvacant = 'N' then 'No'
						else soldasvacant
						end

------------------------------------------------------------------------------------------------------------------------------------

--Remove Duplicates

-- use cte
with rownumCTE as
(
select *,
	Row_Number() over (partition by parcelid,propertyaddress,saleprice,saledate,legalreference
						order by uniqueid) row_num

from [PortfolioProject ]..NashvilleHousing
--order by parcelid
)
delete from rownumCTE
where row_num > 1
--order by propertyaddress


select * from rownumCTE
where row_num > 1
order by propertyaddress


---------------------------------------------------------------------------------------------------------------------------------------

-- Delete Unused Columns

select * from [PortfolioProject ]..NashvilleHousing

Alter table portfolioproject..NashvilleHousing
Drop column owneraddress, Taxdistrict,propertyaddress,saledate

select * from [PortfolioProject ]..NashvilleHousing