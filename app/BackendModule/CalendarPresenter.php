<?php

namespace App\BackendModule;

use App,
	App\Factories\ICalendarListFactory,
	App\Factories\ManageCalendarFormFactory;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class CalendarPresenter extends SecuredPresenter
{
	/** @persistent int */
	public $id;

	/** @var App\Database\Entities\CalendarEntity @autowire */
	protected $calendarEntity;


	public function startup()
	{
		parent::startup();

		if ($this->view != "edit") {
			$this->id = null;
		}
	}


	public function actionEdit($id)
	{
		$this->template->calendar = $this->calendarEntity->find($id);
		if (!$this->template->calendar) {
			$this->redirect("default");
		}

		$defaults = $this->template->calendar->toArray();

		$this["manageCalendarForm"]->setDefaults($defaults);
	}


	protected function createComponentCalendarList(ICalendarListFactory $factory)
	{
		return $factory->create();
	}


	protected function createComponentManageCalendarForm(ManageCalendarFormFactory $factory)
	{
		return $factory->create($this->id);
	}
}
