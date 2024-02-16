select * from PortfolioProject.dbo.CovidDeaths
order by 3,4 

select * from PortfolioProject..covidVaccinations
order by 3,4

-- Select the required Data

select location,date,total_cases,new_cases,total_deaths,population from [PortfolioProject ]..CovidDeaths
order by 1,2

-- Looking at Total Cases vs Total Deaths in United states

Select Location , date ,total_cases,total_deaths,(cast(total_deaths as float)/cast(total_cases as float))*100 as DeathPercentage from [PortfolioProject ]..CovidDeaths
Where location like '%states%'
order by 1,2

-- Looking at Total Cases vs Total Deaths in India

Select Location ,date ,total_cases,total_deaths,(cast(total_deaths as float)/cast(total_cases as float))*100 as DeathPercentage from [PortfolioProject ]..CovidDeaths
Where location like '%india%'
order by 1,2



--Looking at Total cases vs Population  in India

Select Distinct date,location ,total_cases,total_deaths,population,(cast(total_cases as float)/cast(population as float))*100 as CovidPercentage from [PortfolioProject ]..CovidDeaths
Where location like '%india%'
order by 1,2

--Looking at Total cases vs Population  in USA

Select Location ,date ,total_cases,total_deaths,population,(cast(total_cases as float)/cast(population as float))*100 as CovidPercentage from [PortfolioProject ]..CovidDeaths
Where location like '%states%'
order by 1,2

--Looking at Countries with Highest Infection Rate  compared to Population

select location, population ,max(total_cases) as HighestInfectedCount , Max((total_cases / population)*100) as PercentPopulationInfected from [PortfolioProject ]..CovidDeaths
group by location,population
order by PercentPopulationInfected Desc

--Showing Countries with Highest Death Count per Population

select location,max(cast(total_deaths as Int)) as TotalDeathCount from [PortfolioProject ]..CovidDeaths
where continent is not null
group by location
order by TotalDeathCount Desc

--Showing Continents with Highest Death per population

select continent,max(cast(total_deaths as Int)) as TotalDeathCount from [PortfolioProject ]..CovidDeaths
where continent is not null
group by continent
order by TotalDeathCount Desc


--Global numbers in cases and deaths

select sum(new_cases) as TotalCases, sum(cast(new_deaths as Int)) as TotalDeaths , sum(cast(new_deaths as Int))/sum(new_cases) as DeathPercentage
from [PortfolioProject ]..CovidDeaths
where continent is not null
order by 1,2

--Looking at Total Population Vs Vaccination

select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date) 
as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100 
from [PortfolioProject ]..CovidDeaths as dea
join [PortfolioProject ]..CovidVaccinations as vac
on dea.location = vac.location and dea.date = vac.date
where dea.continent is not null

--Using CTE

with PopvsVac(continent,location,date,population,new_vaccinations,RollingPeopleVaccinated)
as
(
select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date) 
as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100 
from [PortfolioProject ]..CovidDeaths as dea
join [PortfolioProject ]..CovidVaccinations as vac
on dea.location = vac.location and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
select *,(RollingPeopleVaccinated/population)*100
from PopvsVac

--Temp Table
drop table if exists #PercentPopulationVaccinated

create table #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date) 
as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100 
from [PortfolioProject ]..CovidDeaths as dea
join [PortfolioProject ]..CovidVaccinations as vac
on dea.location = vac.location and dea.date = vac.date
--where dea.location like '%states%
--order by 2,3
select *,(RollingPeopleVaccinated/population)*100
from #PercentPopulationVaccinated



---Creating View to store Data for Later Visualization

create view  PercentPeoplevaccinate1 as
select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date) 
as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100 
from [PortfolioProject ]..CovidDeaths as dea
join [PortfolioProject ]..CovidVaccinations as vac
on dea.location = vac.location and dea.date = vac.date
where dea.continent is not null
--order by 2,3
select * from  PercentPeoplevaccinate1











