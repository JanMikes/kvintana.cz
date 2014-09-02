<?php

namespace App\Factories;

use Nette,
	App,
	App\Database\Entities\CalendarEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ManageCalendarFormFactory extends Nette\Object
{
	use TFormSaveHandlers;


	/** @var App\Factories\FormFactory */
	private $formFactory;

	/** @var App\Database\Entities\CalendarEntity */
	private $calendarEntity;

	/** @var Nette\Database\Table\ActiveRow */
	private $row;


	public function __construct(
		FormFactory $formFactory,
		CalendarEntity $calendarEntity
	) {
		$this->formFactory = $formFactory;
		$this->calendarEntity = $calendarEntity;
	}


	public function create($id)
	{
		if ($id) {
			$this->row = $this->calendarEntity->find($id);
		}

		$form = $this->formFactory->create();


		$form->addText("date", "Datum a čas", 20, 20)
			->setRequired("Datum a čas je povinný!");

		$form->addText("name", "Název, místo", 100, 100)
			->setRequired("Název je povinný!");

		$form->addTextarea("text", "Bližší info", 60, 3);

		$form->addSubmit("send", $this->row ? "Upravit" : "Přidat")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->save;

		if ($this->row) {
			$form->addSubmit("sendAndContinue", "Uložit a pokračovat v editaci")
				->setAttribute("class", "btn-primary")
				->onClick[] = $this->saveAndContinue;
		}

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);

		if (!$this->row) {
			$values["ins_process"] = __METHOD__;
			$this->calendarEntity->insert($values);
		} else {
			$values["upd_process"] = __METHOD__;
			$this->row->update($values);
		}

	}

}
