<?php

namespace App\Factories;

use Nette,
	App,
	App\Database\Entities\OfferEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ManageOfferFormFactory extends Nette\Object
{
	use TFormSaveHandlers;


	/** @var App\Factories\FormFactory */
	private $formFactory;

	/** @var App\Database\Entities\OfferEntity */
	private $offerEntity;

	private $row;


	public function __construct(
		FormFactory $formFactory,
		OfferEntity $offerEntity
	) {
		$this->formFactory = $formFactory;
		$this->offerEntity = $offerEntity;
	}


	public function create($id)
	{
		if ($id) {
			$this->row = $this->offerEntity->find($id);
		}

		$form = $this->formFactory->create();

		$form->addTextarea("text", "Text", 50, 4)
			->setAttribute("class", "ckeditor");

		
		$form->addSubmit("sendAndContinue", "Uložit")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->saveAndContinue;

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);

		if (!$this->row) {
			$values["ins_process"] = __METHOD__;
			$this->offerEntity->insert($values);
		} else {
			$values["upd_process"] = __METHOD__;
			$this->row->update($values);
		}
	}

}
